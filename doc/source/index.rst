.. .. image:: images/tcfd.png
..    :alt: TrioCFD official logo
..    :width: 600px
..    :align: center

TrioCFD Documentation
---------------------


**TrioCFD** is an open-source software for numerical simulation in fluid mechanics based on the TRUST software platform. It has been developed by the Thermohydraulics and Fluid Mechanics Department (STMF) of ISAS at the Energy Department (DES) of the CEA since 1995. TrioCFD is an object-oriented code, implemented in C++, massively parallel, dedicated to various scientific and industrial studies, as well as research applications.


Some important pages:

- To start using TrioCFD:
   - :ref:`Get started with TrioCFD<quickstart-target>`
   - :ref:`Tutorials<tutorials>`
- To understand the methods of TrioCFD:
   - :ref:`Physical models<physical-models-target>`
   - :ref:`Numerical methods<numerical-methods-target>`
- To help navigating the doc:
   - :ref:`Index<genindex>`
   - :ref:`Search feature<search>`
- References:
   - :ref:`bibliography`: history of PhD thesis using TrioCFD.


Here are some useful links that you can visit too:

* TrioCFD source code: https://github.com/cea-trust-platform/TrioCFD-code
* TrioCFD Website: https://triocfd.cea.fr/
* TrioCFD Support: trust@cea.fr

-----

Table Of Contents
-----------------

.. toctree::
   :titlesonly:

   srcs/user_guide/quickstart.md

.. toctree::
   :maxdepth: 2
   :caption: TrioCFD User Guide
   :titlesonly:
   :includehidden:

   srcs/user_guide/howto/index.rst
   srcs/user_guide/physicalModels/index.rst
   srcs/user_guide/numerical_methods/index.md
   srcs/user_guide/kw-reference/index.md

.. toctree::
   :maxdepth: 2
   :caption: TrioCFD Tutorials
   :titlesonly:
   :includehidden:

   srcs/tutorials/index.rst

.. toctree::
   :maxdepth: 2
   :caption: Developer Corner
   :titlesonly:

   srcs/developer_guide/index.rst
   srcs/developer_guide/FAQ/index.md
   srcs/generated/doxygen/index.rst


.. toctree::
   :maxdepth: 2
   :caption: Navigation
   :includehidden:

   srcs/Bibliography/index
   genindex
   search
