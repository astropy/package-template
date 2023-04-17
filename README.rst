Astropy package template
========================

|powered|   -   **cookiecutter branch:** |ci cookiecutter|

Pending Deprecation Warning
---------------------------
This template is in the process of being subsumed by the 
`OpenAstronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`__,
which reflects more up-to-date Python packaging techniques than this template. In 
the future this template may be replaced by a guide built from the OA guide specific
to Astropy, but in the meantime, if you are starting a new project you may wish to
start from the OA guide.


Introduction
------------

This is a package template provided by the Astropy project.

Using this template, packages can make use of the setup, installation, and documentation
infrastructure developed for the ``astropy`` core and affiliated packages.

For more information, see:

* The `documentation for this package template itself  <http://docs.astropy.org/projects/package-template/en/latest/>`_
* Astropy `documentation about this template <http://docs.astropy.org/en/latest/development/astropy-package-template.html>`_
* `The Affiliated Packages section of the Astropy web site <http://affiliated.astropy.org>`_
* `This template's Github code repository <https://github.com/astropy/package-template>`_


Using this package template
---------------------------

Using cookiecutter
^^^^^^^^^^^^^^^^^^

This package template makes use of the `cookiecutter
<https://cookiecutter.readthedocs.io/en/latest/index.html>`__ package to
make it easier to get started with the package template. You will need to
`install cookiecutter
<https://cookiecutter.readthedocs.io/en/latest/installation.html>`__ which
can be done easily using conda or pip::

  conda install -c conda-forge cookiecutter gitpython

  pip install cookiecutter gitpython


Once you have cookiecutter installed you can run::

  cookiecutter gh:astropy/package-template

Which will ask you a series of questions to configure your package.


Manually
^^^^^^^^

The ``master`` git branch of this repository contains a version of the
template populated with placeholders.  This allows the package template to be
used directly without using cookiecutter, although a number of
`manual steps  <http://docs.astropy.org/projects/package-template/en/latest/>`_
are required.  For this reason the cookiecutter approach is recommended.



Improving the package template
------------------------------

If you want to modify this package template to add or fix things, the folder that
the user ends up with is ``{{ cookiecutter.package_name }}`` in this
repository. Everything in the repository that is not in this folder is not part
of the template that the user will have rendered.

For further information on writing templates for cookiecutter see `the cookiecutter docs <https://cookiecutter.readthedocs.io/en/latest/first_steps.html>`__.


.. |powered| image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

.. |ci cookiecutter| image:: https://github.com/astropy/package-template/workflows/CI/badge.svg
    :target: https://github.com/astropy/package-template/actions
    :alt: CI cookiecutter badge
