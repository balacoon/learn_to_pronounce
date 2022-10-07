"""
Copyright 2022 Balacoon

Interactive pronunciation generation with trained FST
for demo/testing purposes
"""

import logging
import argparse

from balacoon_frontend import FSTPronunciationGenerator, Word


def parse_args():
    ap = argparse.ArgumentParser("Generates pronunciation given FST. WARNING: No input validation in this demo.")
    ap.add_argument("--fst", required=True, help="Path to FST model")
    args = ap.parse_args()
    return args


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    generator = FSTPronunciationGenerator(args.fst)
    while True:
        word_str = input("Enter word: ")
        if not word_str:
            logging.info("No pronunciation for empty string")
        word = Word(word_str)
        generator.phoneticize(word)
        pronunciation = word.get_pronunciation().to_string()
        logging.info(pronunciation)

