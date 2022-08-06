"""
Copyright 2022 Balacoon

Convertor from ARPABet to IPA or X-SAMPA
TODO: Move conversion between phoneme sets to pronunciation_generation package
"""

from typing import List


class ARPAbetConvertor:
    """
    Converts ARPAbet (phonemeset of CMUDict) to more universal IPA or X-SAMPA.
    X-SAMPA - is unicode-friendly version of IPA (international pronunciation alphabet).
    ARPAbet: https://en.wikipedia.org/wiki/ARPABET
    IPA: https://en.wikipedia.org/wiki/International_Phonetic_Alphabet
    X-SAMPA: https://en.wikipedia.org/wiki/X-SAMPA
    Conversion notes: https://github.com/menelik3/cmudict-ipa, https://github.com/Epicalert/xsampadict.
    One modification to IPA/XSAMPA notation: stress marks are put just before vowel, not before syllable.
    That helps to treat stressed/unstressed vowels as separate phonemes for g2p training/forced alignment purposes
    """
    def __init__(self):
        # https://github.com/menelik3/cmudict-ipa/issues/2
        # https://github.com/danmysak/multilingual-ipa-data/blob/main/cmudict/collection/data/phonemes
        # exceptions from https://github.com/menelik3/cmudict-ipa
        self._arpa2ipa = {
            "AA": ["ɑ:"],
            "AE": ["æ"],
            "AH0": ["ə"],
            "AH2": ["ə"],
            "AH1": ["ʌ"],
            "AO": ["ɔ"],
            "AW": ["a", "ʊ̯"],
            "AY": ["a", "ɪ̯"],
            "B": ["b"],
            "CH": ["t", "ʃ"],
            "D": ["d"],
            "DH": ["ð"],
            "EH": ["ɛ"],
            "ER0": ["ɚ"],
            "ER": ["ɝ:"],
            "EY": ["e", "ɪ̯"],
            "F": ["f"],
            "G": ["ɡ"],
            "HH": ["h"],
            "IH": ["ɪ"],
            "IY": ["i:"],
            "JH": ["d", "ʒ"],
            "K": ["k"],
            "L": ["l"],
            "M": ["m"],
            "N": ["n"],
            "NG": ["ŋ"],
            "OW": ["o", "ʊ̯"],
            "OY": ["ɔ", "ɪ̯"],
            "P": ["p"],
            "R": ["ɹ"],
            "S": ["s"],
            "SH": ["ʃ"],
            "T": ["t"],
            "TH": ["θ"],
            "UH": ["ʊ"],
            "UW": ["u:"],
            "V": ["v"],
            "W": ["w"],
            "Y": ["j"],
            "Z": ["z"],
            "ZH": ["ʒ"],
            "<eps>": ["<eps>"],
        }
        self._arpa2ipa_stress = {"0": "", "1": "ˈ", "2": "ˌ"}

        # https://en.wikipedia.org/wiki/X-SAMPA
        self._ipa2xsampa = {
            "ɑ": "A",
            "ɪ̯": "I",
            "æ": "{",
            "ʌ": "V",
            "ə": "@",
            "ɔ": "O",
            "a": "a",
            "ʊ̯": "U",
            "ɪ": "I",
            "b": "b",
            "t": "t",
            "ʃ": "S",
            "d": "d",
            "ð": "D",
            "ɛ": "E",
            "ɚ": "@`",
            "ɝ": "@`",
            "e": "e",
            "f": "f",
            "ɡ": "g",
            "h": "h",
            "i": "i",
            "ʒ": "Z",
            "k": "k",
            "l": "l",
            "m": "m",
            "n": "n",
            "ŋ": "N",
            "o": "o",
            "p": "p",
            "ɹ": "r\\",
            "s": "s",
            "θ": "T",
            "u": "u",
            "ʊ": "U",
            "v": "v",
            "w": "w",
            "j": "j",
            "z": "z",
            "<eps>": "<eps>",
        }
        self._ipa2xsampa_stress = {"ˈ": "\"", "ˌ": "%"}

    def arpa2ipa(self, arpa_phonemes: List[str]) -> List[str]:
        ipa_phonemes = []
        for x in arpa_phonemes:
            # check if its already there without removing a stress
            ipa_x = self._arpa2ipa.get(x, None)

            # convert stress to ipa if any
            ipa_stress = ""
            if x[-1].isdigit():
                ipa_stress = self._arpa2ipa_stress[x[-1]]
                x = x[:-1]

            # if ipa phoneme was not found, look up for phoneme without stress (should be there)
            if ipa_x is None:
                assert x in self._arpa2ipa, "Cant find [{}] in ARPAbet to IPA mapping".format(x)
                ipa_x = self._arpa2ipa[x]

            # add ipa version of stress
            ipa_x = list(ipa_x)
            ipa_x[0] = ipa_stress + ipa_x[0]
            ipa_phonemes.extend(ipa_x)
        return ipa_phonemes

    @staticmethod
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)

    def ipa2xsampa(self, ipa_phonemes: List[str]) -> List[str]:
        xsampa_phonemes = []
        for x in ipa_phonemes:

            # convert stress if any
            xsampa_stress = ""
            if x[0] in self._ipa2xsampa_stress:
                xsampa_stress = self._ipa2xsampa_stress[x[0]]
                x = x[1:]

            # transfer prolongation
            xsampa_prolongation = ""
            if x[-1] == ":":
                xsampa_prolongation = ":"
                x = x[:-1]

            # convert ipa to xsampa
            assert x in self._ipa2xsampa, "Cant find [{}] in IPA to X-SAMPA mapping".format(x)
            xsampa_x = xsampa_stress + self._ipa2xsampa[x] + xsampa_prolongation
            assert is_ascii(xsampa_x), "X-SAMPA phoneme is non-ASCII: {}".format(xsampa_x)
            xsampa_phonemes.append(xsampa_x)

        return xsampa_phonemes

    def arpa2xsampa(self, arpa_phonemes: List[str]) -> List[str]:
        ipa_phonemes = self.arpa2ipa(arpa_phonemes)
        return self.ipa2xsampa(ipa_phonemes)
