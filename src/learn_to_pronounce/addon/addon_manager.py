"""
Copyright 2022 Balacoon

manager that saves artifacts into addon
"""

import os
import shutil
from typing import Any, Dict, List

import msgpack
from pronunciation_generation import PronunciationDictionary
from pronunciation_generation import PronunciationManager as pm


class AddonManager(object):
    """
    Manages addon creation, specifically adds all the necessary fields and artifacts.
    Addon later can be used with pronunciation_generation package.
    The work-flow - is that at each step of pronunciation learning recipe,
    addon is loaded, new artifact is added and addon is saved. In that way, one
    can restart addon building from any step.
    """

    ADDON_FILE_NAME = "pronunciation.addon"

    def __init__(self, work_dir: str, locale: str):
        """
        constructor of addon manager

        Parameters
        ----------
        work_dir: str
            directory where all the temporal artifacts are stored
        locale: str
            locale of the pronunciation generation addon, for ex. en_us
        """
        self._path = os.path.join(work_dir, self.ADDON_FILE_NAME)
        if not os.path.isfile(self._path):
            # there is no addon in work dir, create a dummy one
            addon_dict = {
                pm.addon_field_to_string(pm.AddonFields.ID): pm.addon_identifier(),
                pm.addon_field_to_string(pm.AddonFields.LOCALE): locale,
            }
            self._save_addon_dict(addon_dict)
        else:
            # there is already addon file, verify that locale is the same as current one
            addon_dict = self._load_addon_dict()
            addon_locale = addon_dict[pm.addon_field_to_string(pm.AddonFields.LOCALE)]
            if addon_locale != locale:
                raise RuntimeError(
                    "Addon file exists and locale inside [{}] doesn't match one specified [{}].".format(
                        addon_locale, locale
                    )
                )

    def _load_addon_dict(self) -> Dict[str, Any]:
        """
        Helper function that loads addon as a dictionary
        """
        with open(self._path, "rb") as fp:
            addon_dict = msgpack.load(fp)
        return addon_dict

    def _save_addon_dict(self, addon_dict: Dict[str, Any]):
        """
        Helper function that stores dictionary as an addon
        """
        with open(self._path, "wb") as fp:
            msgpack.dump(addon_dict, fp)

    def save(self, path: str):
        """
        Copies addon to the specified path

        Parameters
        ----------
        path: str
            path to copy addon to
        """
        shutil.copy(self._path, path)

    def add_lexicon(
        self, pd: PronunciationDictionary, graphemes: List[str], phonemes: List[str]
    ):
        """
        Adds lexicon into addon. Also adds corresponding graphemes and phonemes

        Parameters
        ----------
        pd: PronunciationDictionary
            parsed lexicon that should be added into addon
        graphemes: List[str]
            list of valid graphemes (letters)
        phonemes: List[str]
            list of valid phonemes
        """
        addon_dict = self._load_addon_dict()
        addon_dict[pm.addon_field_to_string(pm.AddonFields.LEXICON)] = pd.serialize()
        addon_dict[pm.addon_field_to_string(pm.AddonFields.GRAPHEMES)] = graphemes
        addon_dict[pm.addon_field_to_string(pm.AddonFields.PHONEMES)] = phonemes
        self._save_addon_dict(addon_dict)

    def _add_fst(self, key: str, fst_path: str):
        """
        Helper function that adds FST model into addon

        Parameters
        ----------
        key: str
            key under which to store FST
        fst_path: str
            path to FST model to load and add to addon
        """
        addon_dict = self._load_addon_dict()
        with open(fst_path, "rb") as fp:
            fst_data = fp.read()
        addon_dict[key] = fst_data
        self._save_addon_dict(addon_dict)

    def add_pronunciation_fst(self, fst_path: str):
        """
        Adds pronunciation FST into addon

        Parameters
        ----------
        fst_path: str
            path to FST model
        """
        self._add_fst(
            pm.addon_field_to_string(pm.AddonFields.FST_PRONUNCIATION_GENERATOR),
            fst_path,
        )

    def add_spelling_fst(self, fst_path: str):
        """
        Adds spelling FST into addon

        Parameters
        ----------
        fst_path: str
            path to FST model
        """
        self._add_fst(
            pm.addon_field_to_string(pm.AddonFields.FST_SPELLING_GENERATOR), fst_path
        )
