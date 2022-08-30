# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'learn_to_pronounce'
copyright = '2022, Balacoon'
author = 'Clement Ruhm'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', "numpydoc", "sphinx.ext.coverage", "sphinx.ext.viewcode"]

templates_path = ['_templates']

autosummary_generate = True
numpydoc_show_class_members = False

autodoc_default_options = {"inherited-members": False}

exclude_patterns = []

autodoc_mock_imports = ["balacoon_pronunciation_generation", "tqdm"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
