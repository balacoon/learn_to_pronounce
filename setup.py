# -*- coding: utf-8 -*-
# Copyright 2022 Balacoon

from setuptools import setup, find_packages


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(
    name="learn_to_pronounce",
    version="0.0.1",
    author="Clement Ruhm",
    author_email="clement@balacoon.com",
    description="Module for training artifacts for pronunciation_generation",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://balacoon.com/",
    # declare your packages
    packages=find_packages(where="src", exclude=("test",)),
    package_dir={"": "src"},
    # declare your scripts
    entry_points="""\
     [console_scripts]
     learn_to_pronounce = learn_to_pronounce.learn_to_pronounce:main
    """
)

