# Copyright 2022 Balacoon

import os
import msgpack
import tempfile

from pronunciation_generation import PronunciationDictionary
from pronunciation_generation import PronunciationManager as pm

from learn_to_pronounce.addon.addon_manager import AddonManager


def _load_addon(addon_path):
    assert os.path.isfile(addon_path)
    with open(addon_path, "rb") as fp:
        addon_sections = msgpack.load(fp)
    assert len(addon_sections) == 1
    addon = addon_sections[0]
    return addon


def test_addon_manager():
    temp_dir = tempfile.TemporaryDirectory()
    am = AddonManager(temp_dir.name, "en_us")

    addon_path = os.path.join(temp_dir.name, am.ADDON_FILE_NAME)
    addon = _load_addon(addon_path)
    id_field = pm.addon_field_to_string(pm.AddonFields.ID)
    assert id_field in addon
    assert addon[id_field] == pm.addon_identifier()
    locale_field = pm.addon_field_to_string(pm.AddonFields.LOCALE)
    assert locale_field in addon
    assert addon[locale_field] == "en_us"

    am.add_lexicon(PronunciationDictionary(), [], [])
    addon = _load_addon(addon_path)
    assert pm.addon_field_to_string(pm.AddonFields.LEXICON) in addon
    for field in [pm.AddonFields.PHONEMES, pm.AddonFields.GRAPHEMES]:
        field_str = pm.addon_field_to_string(field)
        assert field_str in addon
        assert len(addon[field_str]) == 0

    am.add_pronunciation_fst(addon_path)
    addon = _load_addon(addon_path)
    pron_fst_field = pm.addon_field_to_string(pm.AddonFields.FST_PRONUNCIATION_GENERATOR)
    spel_fst_field = pm.addon_field_to_string(pm.AddonFields.FST_SPELLING_GENERATOR)
    assert pron_fst_field in addon
    assert spel_fst_field not in addon

    am.add_spelling_fst(addon_path)
    addon = _load_addon(addon_path)
    assert pron_fst_field in addon
    assert spel_fst_field in addon

    temp_dir.cleanup()
