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
# or
pip install -r doc/requirements.txt
cd doc
make html
```
Use your web browser to open the index file located at `build/html/index.html`.

To produce a pdf, one must have `latexmk` installed and run `make latexpdf`.

## Edition
Two formats can be used in Sphinx, [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) and [Markdown](https://www.markdownguide.org/). The complete markdown syntax is described by the [MyST Syntaxe Guide](https://myst-parser.readthedocs.io/en/v0.13.7/using/syntax.html).

To write math, the dollar separated syntax from LaTeX works as well as environment like `\begin{align}`. One can also write in markdown without latex
```
{math}`k-\varepsilon`
```
to produce $k-\varepsilon$. But the dollar separated syntax from LaTeX also works, as well as the environment like `\begin{align}`.

The bibliography is managed by a [bibtex sphinx module](https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html). In markdown, one must use `{cite:t}` to produce *Author et al. [key]*.

## ReadTheDocs
The website is deployed on readthedocs.

Build and deploy is triggered automatically when pushing on master branch.

Build status is available at https://app.readthedocs.org/projects/triocfd-documentation/builds/.
