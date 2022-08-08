"""
Copyright 2022 Balacoon

Custom resource provider for tests
"""

from typing import Iterable
import json

from learn_to_pronounce.resources.provider import DefaultProvider
from pronunciation_generation import PronunciationDictionary


class CustomProvider(DefaultProvider):
    LEXICON_FILE_NAME = "dictionary"

    def parse_lexicon(
        self, path: str, words: Iterable[str] = None
    ) -> PronunciationDictionary:
        if words:
            words = set(words)
        pd = PronunciationDictionary()

        with open(path, "r", encoding=self._encoding) as fp:
            loaded = json.load(fp)
            for word in loaded:
                assert len(word) == 1
                word_str = next(iter(word.keys()))
                if words and word_str not in words:
                    continue
                pronunciations = next(iter(word.values()))
                for pron in pronunciations:
                    pd.add_word(word_str, pron, tag="")

        return pd
