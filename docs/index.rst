.. _package-template:

Welcome to Astropy Package Template's documentation!
====================================================

The Astropy package template is designed to help quickly create new Python
packages within the Astropy ecosystem. This package mirrors the layout of the
main `Astropy_` core library, as well as reusing much of the helper code used to
organize `Astropy_` and many Astropy affiliated packages.

This documentation will guide you through getting started with the package
template and updating your package when the template is updated.

Getting Started
---------------

The Astropy Package template uses the `Cookiecutter
<http://cookiecutter.readthedocs.io/>`_ project to make it easier to customise
the template for your package. To use the package template you need cookiecutter
installed. The package template also optionally makes use of `gitpython
<https://gitpython.readthedocs.io/en/stable/>`_ to setup the 
``astropy_helpers`` submodule. Depending on how you have Python
installed these packages can be obtained through either pip or conda::

  conda install -c conda-forge cookiecutter gitpython

or::

  pip install cookiecutter gitpython


Cookiecutter works by taking a template (in this case the Astropy Package
Template) and asking you a series of :ref:`questions <options>` to create a set
of files and folders where your answers to the questions are pre-filled into the
correct places. The package template uses this to allow you to specify things
like your project's name as well as choose what parts and features of the
template you want to use.

To start a package with the package template run::

  cookiecutter -c cookiecutter gh:astropy/package-template

This will prompt you with a series of questions about your project. See 
the :ref:`options` page for more details on the various options.

If this is the first time you are rendering a template, you may want to take a
moment to examine the example files that have been included in the package.  
These are examples of a pure-python module, a test script, a `Cython
<http://cython.org/>`_ module, and a sub-package, respectively.  These are
provided as examples of a standard way to lay these out. Once you understand
these or if you do not need them, you'll want to delete them 
and later replace with your own as needed.

For further customization of your package including setting up testing and 
documentation, read the :ref:`next-steps` for further information.  

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   options
   nextsteps
   updating



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Astropy: http://astropy.org
