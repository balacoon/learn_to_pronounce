"""
Copyright 2022 Balacoon

Recipe to build an addon for pronunciation_generation.
"""

import os
import argparse

from learn_to_pronounce.resources import get_provider
from learn_to_pronounce.addon.addon_manager import AddonManager
from learn_to_pronounce.fst.fst_trainer import FSTTrainer, add_fst_arguments


def parse_args():
    ap = argparse.ArgumentParser(description="Learns how to pronounce words, creates artifacts for pronunciation_generation package.",
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--resources", required=True, help="Directory with pronunciation resources. Those are stored in repos that are submodules to this repo.")
    ap.add_argument("--locale", required=True, help='Locale corresponding to resources, that will be stored in addon')
    ap.add_argument("--work-dir", default="work_dir", help="Working directory to put intermediate artifacts to")
    ap.add_argument("--out", help="Path to put produced artifact to. It is also stored at work_dir/addon")
    ap.add_argument("--stage", choices=["lexicon", "spelling", "pronunciation", "all"], default="all",
                    help="Which stage of pronunciation learning to execute:\n"
                    "> lexicon - just pack dictionary for pronunciation look up\n"
                    "> spelling - train small FST model to spell words\n"
                    "> pronunciation - train FST-based pronunciation generation\n"
                    "> all - all of the above")
    add_fst_arguments(ap)
    args = ap.parse_args()
    return args


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    os.makedirs(args.work_dir, exist_ok=True)
    addon_manager = AddonManager(args.work_dir, args.locale)
    provider = get_provider(args.resources)

    if args.stage == "lexicon" or args.stage == "all":
        logging.info("Packing pronunciation dictionary")
        pd = provider.get_lexicon()
        graphemes = provider.get_graphemes()
        phonemes = provider.get_phonemes()
        pd.validate(graphemes, phonemes)
        addon_manager.add_lexicon(pd, graphemes, phonemes)

    if args.stage == "spelling" or args.stage == "all":
        fst_trainer = FSTTrainer(provider, args.work_dir, args)
        logging.info("Training small FST-based spelling model")
        path = fst_trainer.train_spelling()
        addon_manager.add_spelling_fst(path)

    if args.stage == "pronunciation" or args.stage == "all":
        fst_trainer = FSTTrainer(provider, args.work_dir, args)
        logging.info("Training FST-based pronunciation model")
        path = fst_trainer.train_pronunciation()
        addon_manager.add_spelling_fst(path)

    if args.out:
        addon_manager.save(args.out)
