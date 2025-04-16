import sys
import os
sys.path.insert(0, os.path.abspath('..'))
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#


# -- Project information -----------------------------------------------------

project = 'TrioCFD Documentation'
author = 'TrioCFD'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
pygments_style = 'sphinx'
extensions = [
    'sphinx.ext.autodoc',
    # 'numpydoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.napoleon',
    'myst_parser'
]

htmlhelp_basename = 'TrioCFD Documentation'

# To show or not private members
autodoc_default_options = {"members": True,
                           "undoc-members": True,
                           "private-members": False}


# generate autosummary even if no references
numpydoc_show_class_members = False
autosummary_generate = False
autosummary_imported_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# master_doc = 'index'
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = 'sphinx_material'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# pour éviter l'erreur du cache
suppress_warnings = ["config.cache"]

# pour pouvoir écrire du markdown
source_suffix = {'.rst': 'restructuredtext', '.md': 'restructuredtext'}
