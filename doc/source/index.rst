.. .. image:: images/tcfd.png
..    :alt: TrioCFD official logo
..    :width: 600px
..    :align: center

TrioCFD Documentation
---------------------


**TrioCFD** is an open-source software for numerical simulation in fluid mechanics based on the TRUST software platform. It has been developed by the Thermohydraulics and Fluid Mechanics Department (STMF) of ISAS at the Energy Department (DES) of the CEA since 1995. TrioCFD is an object-oriented code, implemented in C++, massively parallel, dedicated to various scientific and industrial studies, as well as research applications.

- :ref:`Get started with TrioCFD<get-started-target>`
- :ref:`Turbulence modeling<turbulence_modeling>`
- :ref:`Multiphase RANS modeling<multiphase_cfd>`
- :ref:`Tutorials<tutorials>`

A history of PhD thesis is given in the :ref:`bibliography` page.

Visiting the :ref:`Index<genindex>` or using the :ref:`Search feature<search>` may help you navigating this documentation.


Here are some useful links that you can visit too:

* TrioCFD source code: https://github.com/cea-trust-platform/TrioCFD-code
* TrioCFD Website: https://triocfd.cea.fr/
* TrioCFD Support: trust@cea.fr

-----

Table Of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :titlesonly:
   :includehidden:
   :numbered:

   srcs/userGuidelines/get-started.md
   srcs/userGuidelines/howto/index.rst
   srcs/userGuidelines/Tutorials/index.rst
   srcs/userGuidelines/physicalModels/index.rst

.. toctree::
   :maxdepth: 2
   :caption: Developer Guidelines
   :titlesonly:
   :numbered:

   srcs/developerGuidelines/setup-git.md
   srcs/developerGuidelines/testing/index.md
   srcs/developerGuidelines/documentation/index.md
   srcs/developerGuidelines/code-syntax/index.md
   srcs/developerGuidelines/git-tutorial/index.rst
   srcs/developerGuidelines/FAQ/index.md

.. toctree::
   :maxdepth: 1
   :caption: Generated Documentation

   srcs/generated/kw-reference/index.md
   srcs/generated/doxygen/index.rst

.. toctree::
   :maxdepth: 2
   :caption: Navigation
   :includehidden:

   srcs/Bibliography/index
   genindex
   search
