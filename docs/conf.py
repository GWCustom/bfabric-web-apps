# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath(r"C:\Users\marc_\Documents\Git\bfabric-web-apps"))

# -- Project information -----------------------------------------------------
project = 'bfabric-web-apps'
copyright = '2024, GWC GmbH'
author = 'Griffin White & Marc Zuber'
release = '20.12.2024'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',         # MyST for Markdown support
    'sphinx.ext.autodoc',  # For API documentation
    'sphinx.ext.napoleon', # For Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode', # Add links to highlighted source code
    'sphinx_copybutton',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'Python'

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'

# Theme options for PyData
html_theme_options = {
    "logo": {
        "image_light": "_static/logo_light.png",
        "image_dark": "_static/logo_dark.png",
    },
    "navbar_end": ["theme-switcher"],
    "use_edit_page_button": False,
    "show_toc_level": 2,  # Reduce TOC depth to avoid long lists
    "secondary_sidebar_items": ["page-toc"],  # Custom sidebar items
    "pygments_light_style": "xcode",
    "pygments_dark_style": "github-dark",
    "default_mode": "dark",
    "show_nav_level": 0,
}


# Add static path for logos and additional static files
html_static_path = ['_static', '_images']
html_css_files = ['sidebar-nav.css', 'custom.css']

# Custom sidebar definition with "Quick Links"
html_sidebars = {
    "**": [
        "custom-quick-links.html",  # Custom quick links
    ]
}

# Optional context for GitHub integration
html_context = {
    "github_url": "https://github.com/GWCustom/bfabric-web-apps",
    "github_user": "GWCustom",
    "github_repo": "bfabric-web-apps",
    "github_version": "main",
    "doc_path": "docs",
}