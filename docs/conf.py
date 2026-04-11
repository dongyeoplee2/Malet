"""Sphinx configuration for Malet documentation."""

import subprocess
import sys
from pathlib import Path

# Auto-generate changelog from git tags before building
_changelog_script = Path(__file__).resolve().parent.parent / "scripts" / "generate_changelog.py"
if _changelog_script.exists():
    subprocess.run([sys.executable, str(_changelog_script)], check=False)

project = "Malet"
copyright = "2024, Dongyeop Lee"
author = "Dongyeop Lee"
release = "0.2.2"

extensions = [
    "myst_parser",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
]

# MyST Markdown settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_heading_anchors = 3

# sphinx-autoapi settings (static analysis, works without __init__.py)
autoapi_type = "python"
autoapi_dirs = ["../src/malet"]
autoapi_root = "api"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_keep_files = False

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Theme — sphinx_book_theme (same as JAX docs)
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_title = "\U0001f528 Malet"
html_logo = "_static/logo/malet.svg"
html_theme_options = {
    "show_toc_level": 2,
    "repository_url": "https://github.com/dongyeoplee2/Malet",
    "use_repository_button": True,
    "navigation_with_keys": False,
}
html_css_files = ["custom.css"]

# Exclude internal planning docs from build
exclude_patterns = ["MALEP.md", "MALET_NOTES.md"]

# Suppress warnings
suppress_warnings = [
    "autoapi.python_import_resolution",
    "myst.xref_missing",
]
nitpicky = False
