"""Sphinx configuration."""
project = "Warehouse Ddd"
author = "Lex Trofimov"
copyright = "2024, Lex Trofimov"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
