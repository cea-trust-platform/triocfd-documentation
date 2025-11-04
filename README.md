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
pip install -r doc/requirements.txt
cd doc
make html
```
Use your web browser to open the index file located at `build/html/index.html`.

To produce a pdf, one must have `latexmk` installed and run `make latexpdf`.

For vscode users, there are also tasks defined: `configure` that create and source venv and install dependencies, `build` (does `make html`) and `open` that directly opens the result in your webbrowser. 

## Edition
Two formats can be used in Sphinx, [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) and [Markdown](https://www.markdownguide.org/). The complete markdown syntax is described by the [MyST Syntaxe Guide](https://myst-parser.readthedocs.io/en/v0.13.7/using/syntax.html).

To write math, the dollar separated syntax from LaTeX works as well as environment like `\begin{align}`. One can also write in markdown without latex
```
{math}`k-\varepsilon`
```
to produce $k-\varepsilon$. But the dollar separated syntax from LaTeX also works, as well as the environment like `\begin{align}`.

The bibliography is managed by a [bibtex sphinx module](https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html). In markdown, one must use `
{cite:t}` to produce *Author et al. [key]*.

## Doxygen and DoxygenToRST

The Doxygen documentation of TRUST and TrioCFD is included in this doc. Documentation of a specific class or function can be cited using the syntax given in the doxygen section. This is done with the external (self-developped) python package [DoxygenToRST](https://github.com/cea-trust-platform/DoxygenToRST).

To ease the further development and testing of DoxygenToRST, a local version can be created and edited using `make updateDoxygenToRST` (in the source subdirectory). The first use of this makefile target will create the local copy and install it. After editing DoxygenToRST sources, it can be reinstalled with the same target (updateDoxygenToRST).

To shorten build time when editing DoxygenToRST, a test mode can be enabled by setting the env variable TEST_RST to 1. A common usage while developing will be:
```
TEST_RST=1 make updateDoxygenToRST html
```
which will update the python package, create the rst files from Doxygen data (in test mode) and rebuild the html website all at once.

Test mode works by filtering the Doxygen files that will be included in the final website. A file named `.doxygen_test_list` must be present beside the `conf.py` file that contains patterns of class/file names that will be included in the test build. In this mode, there will be warning of missing references if the whole inheritance family of a class is not included. This mode is meant mostly to test the visual aspect of the resulting rst files.

## Deployment

The website is deployed on [github-pages](https://cea-trust-platform.github.io/triocfd-documentation/).

Build and deploy is triggered automatically when pushing on master branch, and can also be triggered manually (useful if only DoxygenToRST has changed).

Build status is available [here](https://github.com/cea-trust-platform/triocfd-documentation/actions).

## ReadTheDocs

No longer applies, because build time limitations too strict.

The website is deployed on readthedocs.

Build and deploy is triggered automatically when pushing on master branch.

Build status is available at https://app.readthedocs.org/projects/triocfd-documentation/builds/.
