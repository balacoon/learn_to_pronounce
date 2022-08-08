"""
Resources
=========
Provides interface to resource directory with pronunciation lexicon:
https://github.com/balacoon/en_us_pronunciation/tree/main/cmudict
learn_to_pronounce interacts with data via resource provider.

Abstract resource provider defines methods which are used during
learning pronunciation:

.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: class.rst

    AbstractProvider

Basic implementation of resource provider:

.. autosummary::
    :toctree: generated/
    :nosignatures:
    :template: class.rst

    DefaultProvider

If custom resource directory is used, one can implement their own provider
and put it to resource directory. if custom_provider.py with CustomProvider
class is available in resource directory, it will be used to access the data.
Check https://github.com/balacoon/learn_to_pronounce/blob/main/tests/dummy_data/custom_provider_data/custom_provider.py
for reference.
"""

import importlib.util
import logging
import os
import types

from learn_to_pronounce.resources.provider import AbstractProvider, DefaultProvider


def _get_module_from_file(
    path: str, module_name: str = "custom_provider"
) -> types.ModuleType:
    """
    Helper function to load python model from a file

    Parameters
    ----------
    path: str
        path to a source file to load module form
    module_name: str
        Name for the module being loaded

    Returns
    -------
    module: types.ModuleType
        module loaded from specific source file
    """
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_provider(resources_dir: str) -> AbstractProvider:
    """
    Creates a resource provider for the given resource directory.
    If resource directory contains file `custom_provider.py` with class "CustomProvider"
    defined inside, it will be used to load the data. Otherwise "DefaultProvider" will be used.
    "CustomProvider" should implement methods from "AbstractProvider".

    Parameters
    ----------
    resources_dir: str
        Directory with resources: lexicon, spelling_lexicon, etc

    Returns
    -------
    provider: AbstractProvider
        resource provider, object that implements methods of AbstractProvider,
        which allow to load data from resource directory for pronunciation learning.
    """
    resource_provider = None
    custom_provider_path = os.path.join(resources_dir, "custom_provider.py")
    if os.path.isfile(custom_provider_path):
        logging.info(
            "Trying to use custom resource provider for [{}]".format(resources_dir)
        )
        try:
            custom_provider_module = _get_module_from_file(custom_provider_path)
            resource_provider = custom_provider_module.CustomProvider(resources_dir)
        except AttributeError:
            logging.warning(
                "Couldn't load `CustomProvider` from [{}]. Using default.".format(
                    custom_provider_path
                )
            )

    if resource_provider is None:
        resource_provider = DefaultProvider(resources_dir)

    return resource_provider
