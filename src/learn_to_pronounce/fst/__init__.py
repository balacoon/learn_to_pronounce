"""
FST
===
Interface to train FST-based pronunciation generation.
Phonetisaurus is used https://github.com/AdolfVonKleist/Phonetisaurus
under the hood. FST-based model is used for both spelling and regular pronunciation
training. For spelling, training data should just specify how each letter should be
pronounced. There is also code for evaluation of pronunciation generation algo.
In the future it should generalized to work with any pronunciation generation method.

.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: class.rst

    FSTTrainer
    FSTEvaluator

"""

from learn_to_pronounce.fst.fst_trainer import FSTTrainer
from learn_to_pronounce.fst.fst_evaluator import FSTEvaluator
