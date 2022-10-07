"""
Copyright 2022 Balacoon

Evaluates trained FST model on withhold lexicon
"""

import tqdm
import logging
from typing import List, Tuple

import edlib
from balacoon_frontend import FSTPronunciationGenerator, Pronunciation, PronunciationDictionary, Word


class PronunciationComparator:
    """
    Compares pronunciations, tracks total WER and PER.
    Follows evalution strategy from Phonetisaurus: compares top-1 generated pronunciation with
    all the pronunciations for the given word, selects a pair which is most similar.
    """

    def __init__(self, with_stress=True):
        """
        constructor of pronunciation comporator

        Parameters
        ----------
        with_stress: str
            flag whether to take into account stress when pronunciations are compared
        """
        self._with_stress = with_stress
        self._reset()

    def _reset(self):
        """
        Resets all accumulators for metrics
        """
        self._total_words = 0
        self._correct_words = 0
        self._total_phonemes = 0
        self._incorrect_phonemes = 0

    def compare(
        self,
        reference_pronunciations: List[Pronunciation],
        hypothesis_pronunciation: Pronunciation,
    ):
        """
        Compares pronunciations, updates metrics

        Parameters
        ----------
        reference_pronunciations: List[Pronunciation]
            list of correct pronunciations for given word
        hypothesis_pronunciation: Pronunciation
            hypothesis of pronunciation by PronunciationGenerator
        """
        self._total_words += 1
        self._total_phonemes += reference_pronunciations[0].size()
        min_distance = float("inf")
        min_distance_index = -1
        for i, reference_pronunciation in enumerate(reference_pronunciations):
            reference_phonemes = reference_pronunciation.to_string(
                with_stress=self._with_stress
            ).split()
            hypothesis_phonemes = hypothesis_pronunciation.to_string(
                with_stress=self._with_stress
            ).split()
            distance = edlib.align(hypothesis_phonemes, reference_phonemes)[
                "editDistance"
            ]
            if distance < min_distance:
                min_distance = distance
                min_distance_index = i
            if not distance:
                # correct pronunciation. shortcut to exit function
                self._correct_words += 1
                self._total_phonemes += len(reference_phonemes)
                return

        self._incorrect_phonemes += min_distance
        self._total_phonemes += reference_pronunciations[min_distance_index].size()

    def get_metrics(self) -> Tuple[float, float]:
        """
        returns WER and PER in percents given all compared pronunciations

        Returns
        -------
        wer: float
            word error rate in percent
        per: float
            phoneme error rate in percent
        """
        wer = (
            100.0 * (self._total_words - self._correct_words) / float(self._total_words)
        )
        per = 100.0 * self._incorrect_phonemes / float(self._total_phonemes)
        return wer, per


class FSTEvaluator:
    """
    Evaluates FST given lexicon.
    Prints WER and PER, computed from comparing ground truth pronunciations and generated one
    """

    def __init__(self, fst_path: str):
        """
        constructor of fst evaluator

        Parameters
        ----------
        fst_path: str
            path to FST model to evaluate
        """
        self._fst = FSTPronunciationGenerator(fst_path)

    def evaluate(self, lexicon: PronunciationDictionary):
        """
        Runs evaluation

        Parameters
        ----------
        lexicon: PronunciationDictionary
            words and ground truth pronunciations to evaluate on
        """
        comparator = PronunciationComparator()
        comparator_wo_stress = PronunciationComparator(with_stress=False)
        for ref_word in tqdm.tqdm(lexicon.get_words()):
            hyp_word = Word(ref_word.name())
            self._fst.phoneticize(hyp_word)
            ref_pron = ref_word.get_pronunciations()
            hyp_pron = hyp_word.get_pronunciation()
            comparator.compare(ref_pron, hyp_pron)
            comparator_wo_stress.compare(ref_pron, hyp_pron)

        logging.info("Performance taking into account stress marks:")
        wer, per = comparator.get_metrics()
        logging.info("WER,%: {:.2f}; PER,%: {:.2f}".format(wer, per))
        logging.info(
            "Performance WITHOUT taking into account stress marks (stressless):"
        )
        wer, per = comparator_wo_stress.get_metrics()
        logging.info("WER,%: {:.2f}; PER,%: {:.2f}".format(wer, per))
