"""
Copyright 2022 Balacoon

Small script to convert phonemeset in a lexicon
TODO: Move conversion between phoneme sets to pronunciation_generation package
"""

import argparse

from learn_to_pronounce.phonetics.arpabet_convertor import ARPAbetConvertor


def parse_args():
    ap = argparse.ArgumentParser(description="Helper script that converts phonemeset in a lexicon")
    ap.add_argument("in_path", help="Lexicon to convert")
    ap.add_argument("out_path", help="Path to put converted lexicon to")
    ap.add_argument("--source", help="Source phonemeset", choices=["arpa"], default="arpa")
    ap.add_argument("--target", help="Target phonemeset", choices=["xsampa", "ipa"], default="xsampa")
    args = ap.parse_args()
    return args


def main():
    args = parse_args()
    convertor = ARPAbetConvertor()

    with open(args.in_path, "r", encoding="utf-8") as ifp, open(args.out_path, "w", encoding="utf-8") as ofp:
        for line in ifp:
            parts = line.strip().split("\t")
            arpa_phonemes = parts[-1].split()
            if args.target == "xsampa":
                converted_phonemes = convertor.arpa2xsampa(arpa_phonemes)
            elif args.target == "ipa":
                converted_phonemes = convertor.arpa2ipa(arpa_phonemes)
            else:
                raise RuntimeError("Unsupported target phonemeset: {}".format(args.target))
            parts[-1] = " ".join(converted_phonemes)
            ofp.write("\t".join(parts) + "\n")


if __name__ == "__main__":
    main()
