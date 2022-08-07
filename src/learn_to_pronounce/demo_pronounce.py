"""
Copyright 2022 Balacoon

Interactive pronunciation generation with created addon
"""

import logging
import argparse

from pronunciation_generation import PronunciationManager, Word


def parse_args():
    ap = argparse.ArgumentParser("Returns pronunciation given addon.")
    ap.add_argument(
        "--spelling", action="store_true", help="If specified, words are spelled"
    )
    ap.add_argument(
        "--addon",
        required=True,
        help="Path to pronunciation addon (work_dir/pronunciation.addon",
    )
    ap.add_argument(
        "--locale",
        default="",
        help="If addon has multiple pronunciation fields sections, disambiguate one to use, by providing locale",
    )
    args = ap.parse_args()
    return args


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    pronunciation_manager = PronunciationManager(args.addon, args.locale)
    while True:
        word_str = input("Enter word: ")
        if not word_str:
            logging.info("No pronunciation for empty string")
        word = Word(word_str)
        word.set_to_spell(args.spelling)
        pronunciation_manager.add_pronunciation(word)
        pronunciation = word.get_pronunciation().to_string()
        logging.info(pronunciation)
