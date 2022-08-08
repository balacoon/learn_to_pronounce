# Copyright 2022 Balacoon

import os
import pytest
import tempfile

from learn_to_pronounce.resources import get_provider
from learn_to_pronounce.resources.provider import DefaultProvider


def _create_resource_directory(with_spelling: bool = True, with_word_lists: bool = True, with_unit_lists: bool = True):
    temp_dir = tempfile.TemporaryDirectory()
    with open(os.path.join(temp_dir.name, "lexicon"), "w") as fp:
        fp.write("hello\th @ l \"o U\n")
    if with_spelling:
        with open(os.path.join(temp_dir.name, "spelling_lexicon"), "w") as fp:
            fp.write("h\t\"e I t S\n")
    if with_unit_lists:
        with open(os.path.join(temp_dir.name, "phonemes"), "w") as fp:
            fp.write("h\n@\nl\n\"o\nU\n")
        with open(os.path.join(temp_dir.name, "graphemes"), "w") as fp:
            fp.write("h\ne\nl\no\n")
    if with_word_lists:
        for file_name in ["train_words", "test_words"]:
            with open(os.path.join(temp_dir.name, file_name), 'w') as fp:
                fp.write("hello\n")
    return temp_dir


def test_provider():
    temp_dir = _create_resource_directory()
    provider = DefaultProvider(temp_dir.name)
    assert provider.get_lexicon().size() == 1
    assert provider.get_lexicon(words=["world"]).size() == 0
    assert provider.get_spelling_lexicon().size() == 1
    assert len(provider.get_phonemes()) == 5
    assert len(provider.get_graphemes()) == 4
    assert len(provider.get_train_words()) == 1
    assert provider.get_train_words()[0] == "hello"
    assert len(provider.get_test_words()) == 1
    assert provider.get_test_words()[0] == "hello"
    temp_dir.cleanup()


def test_provider_without_words():
    temp_dir = _create_resource_directory(with_word_lists=False)
    provider = DefaultProvider(temp_dir.name)
    assert len(provider.get_train_words()) == provider.get_lexicon().size()
    assert provider.get_test_words() is None
    temp_dir.cleanup()


def test_provider_without_units():
    temp_dir = _create_resource_directory(with_unit_lists=False)
    provider = DefaultProvider(temp_dir.name)
    # those are not in dir, but created from lexicon
    assert len(provider.get_phonemes()) == 5
    assert len(provider.get_graphemes()) == 4
    temp_dir.cleanup()


def test_provider_without_spelling():
    temp_dir = _create_resource_directory(with_spelling=False)
    provider = DefaultProvider(temp_dir.name)
    with pytest.raises(FileNotFoundError):
        provider.get_spelling_lexicon()
    temp_dir.cleanup()


def test_provider_getter():
    temp_dir = _create_resource_directory()
    provider = get_provider(temp_dir.name)
    assert isinstance(provider, DefaultProvider)
    assert provider.get_lexicon().size() == 1
    temp_dir.cleanup()


def test_custom_provider_getter():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "dummy_data", "custom_provider_data")
    provider = get_provider(data_dir)
    assert provider.get_lexicon().size() == 1
