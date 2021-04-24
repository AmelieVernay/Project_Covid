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
# import os
# import sys
# pip install faculty-sphinx-theme
# import faculty_sphinx_theme
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'vizcovidfr'
copyright = '2021, Foux Quentin ; Llinares Laurent ; Nicolas Alexandre ; Vernay Amelie'
author = 'Foux Quentin ; Llinares Laurent ; Nicolas Alexandre ; Vernay Amelie'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	"faculty_sphinx_theme",
	"sphinx.ext.autodoc",
	"sphinx_gallery.gen_gallery",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'faculty-sphinx-theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = '_static/light_transfer_map.png'

html_theme_options = {
	'logo_only': False,
}

html_css_files = {
	'custom.css',
}


import plotly
import plotly.io as pio
from plotly.io._sg_scraper import plotly_sg_scraper
image_scrapers = ('matplotlib', plotly_sg_scraper,)
pio.renderers.default = 'sphinx_gallery'

sphinx_gallery_conf = {
	'example_dirs': '../examples',
	'gallery_dirs': 'auto_examples',
	'remove_config_comments': True,
	'capture_repr': ('_repr_html_', '__repr__'),
	'image_scrapers': image_scrapers,
}

