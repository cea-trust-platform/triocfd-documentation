# TrioCFD documentation on GitHub & Read the Docs !

<img src="https://github.com/cea-trust-platform/.github/blob/main/profile/tcfd.png?raw=true" style="width:12cm;">

Hi there 👋 and welcome to the **[TrioCFD Documentation](https://triocfd-documentation.readthedocs.io/en/latest/)** project page! The documentation is devoted to describe the [TrioCFD](https://github.com/cea-trust-platform/triocfd-code) fluid dynamics code.

The documentation is built with the the open source **[Sphinx](https://www.sphinx-doc.org/en/master/)** and **[Doxygen](https://www.doxygen.nl/)** projects.

Credits for the open-source **[Sphinx Material Theme](https://github.com/bashtage/sphinx-material/blob/main/LICENSE.md)**, **[Doxygen Awesome Theme](https://jothepro.github.io/doxygen-awesome-css/)** and **[Read The Docs](https://blog.readthedocs.com/website-migration/)** projects.

## Installation
```bash
git clone git@github.com:cea-trust-platform/triocfd-documentation.git
python -m venv .venv
source .venv/bin/activate
pip install sphinx sphinx_material myst_parser
cd doc
make html
```
Use your web browser to open the index file located at `build/html/index.html`.

To produce a pdf, one must have `latexmk` installed and run `make latexpdf`.

## Edition
Two formats can be used in Sphinx, [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) and [Markdown](https://www.markdownguide.org/).
