Welcome to Astropy Package Template's documentation!
====================================================

The Astropy package template is designed to help quickly create new Python packages within the Astropy ecosystem.

Getting Started
---------------

The Astropy Package template uses the `Cookiecutter
<http://cookiecutter.readthedocs.io/>`_ project to make it easier to get
started. To use the package template you need cookiecutter installed, depending
on how you have Python installed it can be obtained through either pip or
conda::

  pip install cookiecutter

or::

  conda install -c conda-forge cookiecutter


Cookiecutter works by taking a template (in this case the Astropy Package
Template) and asking you a series of questions to create a set of files and
folders where your answers to the questions are pre-filled into the correct
places. The package template uses this to allow you to specify things like your
projects name as well as choose what parts and features of the template you want
to use.

To start a package with the package template run::

  cookiecutter gh:astropy/package-template

This will ask you a series of questions, and result in a directory inside your
current working directory that has the name of your project.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   options
   updating



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
