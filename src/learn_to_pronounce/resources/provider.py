"""
Copyright 2022 Balacoon

Abstract class and default implementation
for resource provider - object that reads
pronunciation resources.
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Iterable

from balacoon_pronunciation_generation import PronunciationDictionary


class AbstractProvider(ABC):
    """
    shows what should be implemented in resources directory,
    so it can be used by pronunciation learning recipe.
    """

    def __init__(self, resources_dir: str):
        """
        Parameters
        ----------
        resources_dir: str
            Directory with pronunciation resources (lexicon, phonemes, graphemes, etc)
        """
        self._resources_dir = resources_dir

    @abstractmethod
    def get_phonemes(self) -> List[str]:
        """
        Getter for set of phonemes for given pronunciation resource.

        Returns
        -------
        phonemes: List[str]
            Complete set of phonemes for pronunciation resource.
            If it's not among resources, can be derived from lexicon
        """
        pass

    @abstractmethod
    def get_graphemes(self) -> List[str]:
        """
        Getter for set of graphemes (letters) for given pronunciation resource

        Returns
        -------
        graphemes: List[str]
            Complete set of letters for pronunciation resource.
            Can be derived from lexicon.
        """
        pass

    @abstractmethod
    def get_lexicon(self, words: List[str] = None) -> PronunciationDictionary:
        """
        Getter for lexicon - dictionary where pronunciation for the word can be looked up.

        Parameters
        ----------
        words: List[str] = None
            If provided, filters out all the other words from lexicon, keeping only those in the list.
            Is useful to read lexicon for model training only.

        Returns
        -------
        pd: PronunciationDictionary
            parsed lexicon as PronunciationDictionary (from balacoon_pronunciation_generation) object
        """
        pass

    @abstractmethod
    def get_spelling_lexicon(self) -> PronunciationDictionary:
        """
        Getter for spelling lexicon - dictionary with words being spelled letter by letter, rather than pronounced.
        Usually spelling lexicon is very simple, up to just pronunciations of separate letters.

        Returns
        -------
        sp: PronunciationDictionary
            parsed spelling lexicon, similar to :func:`.get_lexicon`
        """
        pass

    @abstractmethod
    def get_train_words(self) -> List[str]:
        """
        Getter for list of words from lexicon (:func:`.get_lexicon`) that should be used in training of
        pronunciation generation. If list is not explicitly specified in resources directory, all the words from
        lexicon should be used.

        Returns
        -------
        words: List[str]
            list of words to be used in training or None
        """
        pass

    @abstractmethod
    def get_test_words(self) -> Optional[List[str]]:
        """
        Getter for list of words from lexicon (:func:`.get_lexicon`) that should be used for evaluation of
        pronunciation generation. If not specified in resources directory - no evaluation will be carried out.

        Returns
        -------
        words: List[str]
            list of words to be used in evaluation or None
        """
        pass


class DefaultProvider(AbstractProvider):
    """
    default implementation of resources provider. If resources provider is not part of
    resource directory, the default provider will be used. That expects resources to have specific names
    and be formatted in specific way. If custom format for resources is used, custom resource provider should
    be implemented.
    """

    PHONEMES_FILE_NAME = "phonemes"  #: name of the file with list of phonemes
    GRAPHEMES_FILE_NAME = (
        "graphemes"  #: name of the file with list of graphemes (letters)
    )
    LEXICON_FILE_NAME = "lexicon"  #: name of the file with pronunciation dictionary
    SPELLING_LEXICON_FILE_NAME = (
        "spelling_lexicon"  #: name of the file with spelling dictionary
    )
    TRAIN_WORDS = "train_words"  #: name of the file with words to be used for training of pronunciation generation
    TEST_WORDS = "test_words"  #: name of the file with words for evaluation of pronunciation generation

    def __init__(self, resources_dir: str, encoding: str = "utf-8"):
        super().__init__(resources_dir)
        self._encoding = encoding

    def _read_lines(self, path: str) -> List[str]:
        """
        Helper function that reads lines from txt file into list of lines
        """
        with open(path, encoding=self._encoding) as fp:
            lines = [x.strip() for x in fp.readlines()]
            return lines

    @staticmethod
    def parse_lexicon_line(line: str) -> Tuple[str, str, str]:
        """
        Helper function that parses lexicon line

        Parameters
        ----------
        line: str
            line read from lexicon file within :func:`.get_lexicon`

        Returns
        -------
        word: str
            string representation of a word
        tag: str
            tag of the pronunciation, empty string if pronunciation variant is not tagged
        phonemes: str
            phonemes representing pronunciation separated by space
        """
        parts = line.split("\t")
        if len(parts) == 2:
            tag = ""
            word, pronunciation = parts
        elif len(parts) == 3:
            word, tag, pronunciation = parts
        else:
            raise RuntimeError("Failed to parse lexicon line [{}]".format(line))
        return word, tag, pronunciation

    def parse_lexicon(
        self, path: str, words: Iterable[str] = None
    ) -> PronunciationDictionary:
        """
        Helper function that parses lexicon from a file.
        Expected format is:

        <word>\t<tag>\t<pronunciation>

        Where <tag> - is optional, <pronunciation> - sequence of phonemes separated with spaces.

        Parameters
        ----------
        path: str
            path to parse lexicon from
        words: Iterable[str]
            list of words to include into returned PronunciationDictionary or None to include all.

        Returns
        -------
        pd: PronunciationDictionary
            pronunciation dictionary object from balacoon_pronunciation_generation
        """
        if words:
            words = set(words)
        pd = PronunciationDictionary()

        with open(path, "r", encoding=self._encoding) as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                word, tag, phonemes = self.parse_lexicon_line(line)

                if words and word not in words:
                    # skip the word, since its not in the list of requested ones
                    continue

                pd.add_word(word, phonemes, tag=tag)

        return pd

    def get_lexicon(self, words: List[str] = None) -> PronunciationDictionary:
        """
        :func:`AbstractProvider.get_lexicon`
        """
        path = os.path.join(self._resources_dir, self.LEXICON_FILE_NAME)
        if not os.path.isfile(path):
            raise FileNotFoundError(
                "{} is not found in {}".format(
                    self.LEXICON_FILE_NAME, self._resources_dir
                )
            )
        return self.parse_lexicon(path, words=words)

    def get_spelling_lexicon(self) -> PronunciationDictionary:
        """
        :func:`AbstractProvider.get_spelling_lexicon`
        """
        path = os.path.join(self._resources_dir, self.SPELLING_LEXICON_FILE_NAME)
        if not os.path.isfile(path):
            raise FileNotFoundError(
                "{} is not found in {}".format(
                    self.SPELLING_LEXICON_FILE_NAME, self._resources_dir
                )
            )
        return self.parse_lexicon(path)

    def get_phonemes(self) -> List[str]:
        """
        :func:`AbstractProvider.get_phonemes`
        """
        path = os.path.join(self._resources_dir, self.PHONEMES_FILE_NAME)
        if os.path.isfile(path):
            return self._read_lines(path)
        logging.info(
            "File with phonemes is not available, deriving unique phonemes from lexicon"
        )
        phonemes = set()
        pd = self.get_lexicon()
        words = pd.get_words()
        # iterate over words in lexicon
        for word in words:
            pronunciations = word.get_pronunciations()
            # iterate over pronunciations of the given word
            for pron in pronunciations:
                # iterate over phonemes in the given pronunciation
                for phone in pron.to_string(delimiter=" ").split():
                    phonemes.add(phone)
        return sorted(list(phonemes))

    def get_graphemes(self) -> List[str]:
        """
        :func:`AbstractProvider.get_graphemes`
        """
        path = os.path.join(self._resources_dir, self.GRAPHEMES_FILE_NAME)
        if os.path.isfile(path):
            return self._read_lines(path)
        logging.info(
            "File with graphemes is not available, deriving unique phonemes from lexicon"
        )
        letters = set()
        pd = self.get_lexicon()
        words = pd.get_words()
        for word in words:
            for letter in word.name():
                letters.add(letter)
        return sorted(list(letters))

    def get_train_words(self) -> List[str]:
        """
        :func:`AbstractProvider.get_train_words`
        """
        path = os.path.join(self._resources_dir, self.TRAIN_WORDS)
        if os.path.isfile(path):
            return self._read_lines(path)
        logging.info(
            "File with words for pronunciation training is not available, using whole lexicon"
        )
        return [x.name() for x in self.get_lexicon().get_words()]

    def get_test_words(self) -> Optional[List[str]]:
        """
        :func:`AbstractProvider.get_test_words`
        """
        path = os.path.join(self._resources_dir, self.TEST_WORDS)
        if os.path.isfile(path):
            return self._read_lines(path)
        logging.info(
            "File with words for pronunciation generation evaluation is not available"
        )
        return None
