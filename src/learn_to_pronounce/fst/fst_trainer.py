"""
Copyright 2022 Balacoon

trains FST - model to generation pronunciation or spelling
"""

import argparse
import logging
import os
from importlib.machinery import SourceFileLoader

from pronunciation_generation import PronunciationDictionary

from learn_to_pronounce.fst.fst_evaluator import FSTEvaluator
from learn_to_pronounce.resources.provider import AbstractProvider


def add_fst_arguments(parser: argparse.ArgumentParser):
    """
    Adds special arguments specific to FST training into argument parsing

    Parameters
    ----------
    parser: argparse.ArgumentParser
        argument parser from recipe to add special arguments to
    """
    arg_group = parser.add_argument_group("fst")
    arg_group.add_argument(
        "--fst-order",
        default=8,
        type=int,
        help="Maximum N-gram order to be used in FST",
    )
    arg_group.add_argument(
        "--fst-spelling-order",
        default=3,
        type=int,
        help="Maximum N-gram order to be used in spelling FST",
    )


class FSTTrainer:
    """
    Trains FST based on provided lexicon. Training is done with phonetisaurus.
    Can be used to train pronunciation or spelling generation.
    """

    def __init__(
        self, provider: AbstractProvider, work_dir: str, args: argparse.Namespace
    ):
        """
        constructor

        Parameters
        ----------
        provider: AbstractProvider
            resources provider that is used to get specific lexicon for training
        work_dir: str
            directory where all intermediate artifacts are stored
        args: argparse.Namespace
            parsed arguments, containing arguments added in :func:`add_fst_arguments`
        """
        self._provider = provider
        self._work_dir = work_dir
        self._args = args

    @staticmethod
    def _dump_fst_train_data(pd: PronunciationDictionary, path: str):
        """
        Helper function that stores pronunciation dictionary suitalbe for FST training
        """
        with open(path, "w", encoding="utf-8") as fp:
            words = pd.get_words()
            # order of words influences result!
            for word in sorted(words, key=lambda x: x.name()):
                for pronunciation in word.get_pronunciations():
                    fp.write("{}\t{}\n".format(word.name(), pronunciation.to_string()))

    def _train_fst(
        self,
        lexicon: PronunciationDictionary,
        train_data_name: str,
        model_name: str,
        ngram_order: int,
        **phonetisaurus_args
    ) -> str:
        """
        Helper function that trains FST on the given lexicon

        Parameters
        ----------
        lexicon: PronunciationDictionary
            lexicon to train on
        train_data_name: str
            name to give to intermediate file with training data
        model_name: str
            name to give to file with trained model
        ngram_order: int
            maximum n-gram order to be used in the FST training.
            Primary parameter that defines tradeoff between model size and accuracy.
        **phonetisaurus_args:
            other named parameters passed directly to phonetisaurus_train.G2PModelTrainer

        Returns
        -------
        fst_path: str
            path to trained FST model
        """
        train_data_path = os.path.join(self._work_dir, train_data_name)
        self._dump_fst_train_data(lexicon, train_data_path)
        phonetisaurus_train = SourceFileLoader(
            "", "/usr/local/bin/phonetisaurus-train"
        ).load_module()
        phonetisaurus_trainer = phonetisaurus_train.G2PModelTrainer(
            train_data_path,
            dir_prefix=self._work_dir,
            model_prefix=model_name,
            ngram_order=ngram_order,
            **phonetisaurus_args
        )
        phonetisaurus_trainer.TrainG2PModel()
        fst_path = os.path.join(self._work_dir, model_name + ".fst")
        return fst_path

    def train_pronunciation(self) -> str:
        """
        Training pronunciation FST

        Returns
        -------
        fst_path: str
            path to trained pronunciation model
        """
        train_lexicon = self._provider.get_lexicon(
            words=self._provider.get_train_words()
        )
        logging.info(
            "Training pronunciation FST on {} words".format(train_lexicon.size())
        )
        fst_path = self._train_fst(
            train_lexicon,
            train_data_name="pronunciation_training_data",
            model_name="pronunciation",
            ngram_order=self._args.fst_order,
            seq2_del=True,
        )
        return fst_path

    def evaluate_pronunciation(self):
        """
        Evaluates trained model using test_words from resources. Prints results in terms of WER/PER to console.
        """
        fst_path = os.path.join(self._work_dir, "pronunciation.fst")
        if not os.path.isfile(fst_path):
            raise FileNotFoundError("Can't run evalution, missing [{}]. Run training first.".format(fst_path))
        test_words = self._provider.get_test_words()
        if not test_words:
            logging.warning(
                "FST evaluation is enabled, but there is no test words in resource directory"
            )
            return
        test_lexicon = self._provider.get_lexicon(words=test_words)
        logging.info(
            "Evaluating pronunciation FST on {} words".format(
                test_lexicon.size()
            )
        )
        evaluator = FSTEvaluator(fst_path)
        evaluator.evaluate(test_lexicon)

    def train_spelling(self) -> str:
        """
        Training spelling FST

        Returns
        -------
        fst_path: str
            path to trained spelling model
        """
        spelling_lexicon = self._provider.get_spelling_lexicon()
        logging.info(
            "Training spelling FST on {} words".format(spelling_lexicon.size())
        )
        fst_path = self._train_fst(
            spelling_lexicon,
            train_data_name="spelling_training_data",
            model_name="spelling",
            ngram_order=self._args.fst_spelling_order,
            seq2_del=True,
        )
        return fst_path
