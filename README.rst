Astropy affiliated package template
===================================

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

This is the template for affiliated packages of the Astropy project.

Astropy affiliated packages are astronomy-related Python packages that
have requested to be part of the Astropy project’s community.
Such packages can make use of the setup, installation, and documentation
infrastructure developed for the ``astropy`` core package simply by
using this template to lay out the package.

Using this package
------------------

This package makes use of the `cookiecutter
<https://cookiecutter.readthedocs.io/en/latest/index.html>`__ package to make it
easier to get started with the package template. You will need to `install cookiecutter <https://cookiecutter.readthedocs.io/en/latest/installation.html>`__ which can
be done easily using conda or pip::

  conda install cookiecutter

  pip install cookiecutter

Once you have cookiecutter installed you can run::

  cookiecutter gh:astropy/package-template


Which will ask you a series of questions to configure your package. For more information you can see the `package template documentation <>`__.


Improving the package template
------------------------------

If you want to modify this package to add or fix things, the actual folder that
the user ends up with is the ``{{ cookiecutter.package_name }}`` folder in this
repository. Everything in the repository that is not in this folder is not part
of the template that the user will have rendered.

For further information on writing templates for cookiecutter see `the docs <https://cookiecutter.readthedocs.io/en/latest/first_steps.html>`__
