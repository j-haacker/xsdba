#!/usr/bin/env python
#
# xsdba documentation build configuration file, created by
# sphinx-quickstart on Fri Jun  9 13:47:02 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here. If the directory is
# relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
#
import os
import sys
import warnings

sys.path.insert(0, os.path.abspath('..'))

import xarray
from pybtex.plugin import register_plugin
from pybtex.style.formatting.alpha import Style as AlphaStyle
from pybtex.style.labels import BaseLabelStyle

xarray.DataArray.__module__ = "xarray"
xarray.Dataset.__module__ = "xarray"
xarray.CFTimeIndex.__module__ = "xarray"

import xsdba


# -- General configuration ---------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.extlinks',
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    "sphinxcontrib.bibtex",
    'sphinx_codeautolink',
    'sphinx_copybutton',
    "nbsphinx",
]

# suppress "duplicate citation for key" warnings
suppress_warnings = ['bibtex.duplicate_citation']


autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2

# To ensure that underlined fields (e.g. `_field`) are shown in the docs.
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "special-members": False,
}


# Bibliography stuff
# a simple label style which uses the bibtex keys for labels
class XCLabelStyle(BaseLabelStyle):
    def format_labels(self, sorted_entries):
        for entry in sorted_entries:
            yield entry.key


class XCStyle(AlphaStyle):
    default_label_style = XCLabelStyle


register_plugin("pybtex.style.formatting", "xcstyle", XCStyle)
bibtex_bibfiles = ["references.bib"]
bibtex_default_style = "xcstyle"
bibtex_reference_style = "author_year"

intersphinx_mapping = {
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

extlinks = {
    "issue": ("https://github.com/Ouranosinc/xsdba/issues/%s", "GH/%s"),
    "pull": ("https://github.com/Ouranosinc/xsdba/pull/%s", "PR/%s"),
    "user": ("https://github.com/%s", "@%s"),
}

skip_notebooks = os.getenv("SKIP_NOTEBOOKS")
if skip_notebooks or os.getenv("READTHEDOCS_VERSION_TYPE") in [
    "branch",
    "external",
]:
    if skip_notebooks:
        warnings.warn("Not executing notebooks.")
    nbsphinx_execute = "never"
elif os.getenv("READTHEDOCS_VERSION_NAME") in ["latest", "stable"]:
    nbsphinx_execute = "always"
else:
    nbsphinx_execute = "auto"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a dictionary of suffix: filetype
source_suffix = {'.rst': 'restructuredtext'}

# The master toctree document.
# master_doc = 'index'
root_doc = "index"


# General information about the project.
project = 'xsdba'
copyright = "2024, Ouranosinc, Éric Dupuis, Trevor James Smith"
author = "Trevor James Smith"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = xsdba.__version__.split('-')[0]
# The full version, including alpha/beta/rc tags.
release = xsdba.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# Sphinx-intl configuration
gettext_compact = False  # optional

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Theme options are theme-specific and customize the look and feel of a
# theme further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {"style_external_links": True}


# Theme options are theme-specific and customize the look and feel of a theme further.
# For a list of options available for each theme, see the documentation.
html_theme_options = {
    "light_logo": "logos/xsdba-logo-light.png",
    "dark_logo": "logos/xsdba-logo-dark.png",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/Ouranosinc/xsdba",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,  # noqa: E501
            "class": "",
        },
    ],
    "dark_css_variables": {
        "color-background-table-rows-even": "#303335",
        "color-background-table-rows-odd": "#3e3e3e",
        "color-text-table-rows-even": "#fff",
        "color-text-table-rows-odd": "#fff",
        "color-copybutton": "#fff",
        "color-indicator-text": "#cfd0d0",
        "color-indicator-background": "#3e3e3e",
        "color-indicator-widget-text": "#a8a8a8",
        "color-indicator-widget-background": "#303335",
        # Fix for xarray injected theme error in auto*dark mode
        # Note: because these are set with the selector
        #   body:not([data-theme="light"]), any variable that uses them needs to
        #   have a scope smaller than body.
        #   However, the xarray variables that use these are defined in the :root selector,
        #   which is higher than body. We therefore need to redefine them in body.
        #   This is done in xarray.css, included at the bottom of this file.
        # furo issue to track when this is no longer needed:
        #   https://github.com/pradyunsg/furo/discussions/790
        "jp-content-font-color0": "rgba(255, 255, 255, 1)",
        "jp-content-font-color2": "rgba(255, 255, 255, 0.54)",
        "jp-content-font-color3": "rgba(255, 255, 255, 0.38)",
        "jp-border-color0": "#1F1F1F",
        "jp-border-color1": "#1F1F1F",
        "jp-border-color2": "#1F1F1F",
        "jp-layout-color0": "#111111",
        "jp-layout-color1": "#111111",
        "jp-layout-color2": "#313131",
        "jp-layout-color3": "#515151",
    },
    "light_css_variables": {
        "color-background-table-rows-even": "#eeebee",
        "color-background-table-rows-odd": "#f5f5f5",
        "color-text-table-rows-even": "#000",
        "color-text-table-rows-odd": "#000",
        "color-copybutton": "#000",
        "color-indicator-text": "#5a5c63",
        "color-indicator-background": "#eeebee",
        "color-indicator-widget-text": "#2f2f2f",
        "color-indicator-widget-background": "#bdbdbd",
        # (consistency for light and dark themes, so variables are unset when switching to light)
        "jp-content-font-color0": "rgba(0, 0, 0, 1)",
        "jp-content-font-color2": "rgba(0, 0, 0, 0.54)",
        "jp-content-font-color3": "rgba(0, 0, 0, 0.38)",
        "jp-border-color0": "#e0e0e0",
        "jp-border-color1": "#e0e0e0",
        "jp-border-color2": "#e0e0e0",
        "jp-layout-color0": "#ffffff",
        "jp-layout-color1": "#ffffff",
        "jp-layout-color2": "#eeeeee",
        "jp-layout-color3": "#bdbdbd",
    },
}

html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = "logos/xsdba-logo-light.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
if not os.path.exists("_static"):
    os.makedirs("_static")
html_static_path = ["_static"]


# -- Options for HTMLHelp output ---------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'xsdbadoc'


# -- Options for LaTeX output ------------------------------------------


latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    "papersize": "letterpaper",
    # The font size ('10pt', '11pt' or '12pt').
    "pointsize": "10pt",
    # Additional stuff for the LaTeX preamble.
    "preamble": r"""
\renewcommand{\v}[1]{\mathbf{#1}}
\nocite{*}
""",
    # Latex figure (float) alignment
    "figure_align": "htbp",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto, manual, or own class]).
latex_documents = [
    (root_doc, 'xsdba.tex',
     'xsdba Documentation',
     'Trevor James Smith', 'manual'),
]

# -- Options for LaTeX output ------------------------------------------

latex_engine = "pdflatex"
latex_logo = "logos/xsdba-logo-light.png"

# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (root_doc, 'xsdba',
     'xsdba Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (root_doc, 'xsdba',
     'xsdba Documentation',
     author,
     'xsdba',
     'One line description of project.',
     'Miscellaneous'),
]
