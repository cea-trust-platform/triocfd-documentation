# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= -j auto
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# update the installed DoxygenToRST when developping in the package
updateDoxygenToRST: DoxygenToRST
	pip install -I ./DoxygenToRST

# clone DoxygenToRST here to facilitate working on it directly
DoxygenToRST:
	@[ -d "./DoxygenToRST" ] || git clone https://github.com/cea-trust-platform/DoxygenToRST

.PHONY: help Makefile updateDoxygenToRST

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
