# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath(r"C:\Users\marc_\Documents\Git\bfabric-web-apps"))
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'bfabric-web-apps'
copyright = '2024, Marc Zuber'
author = 'Marc Zuber'
release = '20.12.2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',         # MyST for Markdown support
    'sphinx.ext.autodoc',  # For API documentation
    'sphinx.ext.napoleon', # For Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode', # Add links to highlighted source code
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'Python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
