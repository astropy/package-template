.. _package-template:

Welcome to Astropy Package Template's documentation!
====================================================

The Astropy package template is designed to help quickly create new Python
packages within the Astropy ecosystem. This package mirrors the layout of the
main `Astropy_` repository, as well as reusing much of the helper code used to
organize `Astropy_`.

This documentation will guide you through getting started with the package
template and updating your package when the template is updated.

Getting Started
---------------

The Astropy Package template uses the `Cookiecutter
<http://cookiecutter.readthedocs.io/>`_ project to make it easier to customise
the template for your package. To use the package template you need cookiecutter
installed. The package template also optionally makes use of 'gitpython' to
setup the ``astropy_helpers`` submodule. Depending on how you have Python
installed these packages can be obtained through either pip or conda::

  pip install cookiecutter gitpython

or::

  conda install -c conda-forge cookiecutter gitpython


Cookiecutter works by taking a template (in this case the Astropy Package
Template) and asking you a series of :ref:`questions <options>` to create a set
of files and folders where your answers to the questions are pre-filled into the
correct places. The package template uses this to allow you to specify things
like your projects name as well as choose what parts and features of the
template you want to use.

To start a package with the package template run::

  cookiecutter -c cookiecutter gh:astropy/package-template

This prompt you for a series of :ref:`options<options>`,current working
directory that has the name of your project. Once you have rendered the template
read :ref:`next-steps`.

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
