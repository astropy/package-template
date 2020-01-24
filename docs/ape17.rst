APE 17 Migration Guide
======================

.. warning:: This guide is not yet ready for widespread use and may
             still change significantly.

The Astropy project is now transitioning from using astropy-helpers for
infrastructure to more standard Python packaging tools. The motivation
and implications of this are discussed in an Astropy Proposal for
Enhancements: `APE 17: A roadmap for package infrastructure without
astropy-helpers <https://github.com/astropy/astropy-APEs/blob/master/APE17.rst>`__

This page aims to provide a guide to migrating to using the new infrastructure
described in APE 17. We assume that your package is currently using
astropy-helpers and that you have used a version of the Astropy package-template
in the past to set up your package (though this guide might still be useful if
the latter is not the case).

Throughout this guide, we will assume that your package is called ``my-package``
and that the module is called ``my_package``. We deliberately choose a name
where the package name is different from the module name, but for many cases,
these will be the same.

Step 1: Remove astropy-helpers
------------------------------

To remove the astropy-helpers submodule, first, run::

   git rm -r astropy_helpers

if ``astropy_helpers`` was the only submodule in your repository, the
``.gitmodules`` file will be empty, you can remove this if you wish.

Next you should remove the ``ah_bootstrap.py`` file::

   git rm ah_bootstrap.py

You can now commit your changes with::

   git commit -m "Remove astropy-helpers submodule"

Step 2: Update/create ``setup.cfg``
-----------------------------------

The next step is to update make sure that you have a ``setup.cfg`` file
that contains meta-data about the package. If you already have this
file, you will likely need to update it, and if you don’t already have
this file, you will need to create it.

This file should contain at least the following entries::

   [metadata]
   name = my-package
   author = ...
   author_email = ...
   license = ...
   license_file = LICENSE.rst
   url = ...
   description = ...
   long_description = file: README.rst

   [options]
   zip_safe = False
   packages = find:
   install_requires =
       numpy
       astropy
       ...
   python_requires = >=3.6

Replace the ``...`` with the information for your package. Make sure
that ``license_file`` and ``long_description`` have the right filename,
and specify your required dependencies one per line in the
``install_requires`` section. Make sure the ``python_requires`` line is
set to indicate the correct minimum Python version for your package.

If you already had a file, make sure you remove the following entries
(if present):

-  ``package_name``
-  ``version``
-  ``setup_requires``
-  ``tests_require``
-  ``[ah_bootstrap]`` and all entries in it

Step 3 - Define optional, test, and docs dependencies
-----------------------------------------------------

Next up, add a new section to the ``setup.cfg`` file (or modify, if it
already exists), to specify optional dependencies as well as
dependencies required to run tests and build the documentation, for
example::

   [options.extras_require]
   all =
       scipy
       matplotlib
   test =
       pytest-astropy
   docs =
       sphinx-astropy

If you don’t need any optional dependencies, remove the ``all`` section.
You will likely need to have at least ``pytest-astropy`` in the ``test``
section and ``sphinx-astropy`` in ``docs``.

Step 4 - Define package data
----------------------------

If your package includes non-Python data files, you will need to update
how you declare which data files to include. If you have been using the
Astropy package template, it is likely that you have functions called
``get_package_data`` defined inside ``setup_package.py`` files. Remove
these functions, and instead define the package data using a
``[options.package_data]`` section inside your ``setup.cfg`` file,
e.g.::

   [options.package_data]
   * = *.fits, *.csv
   my_package.tests = data/*

In the above example, all ``.fits`` and ``.csv`` in the package will be
included as well as all files inside ``my_package/tests/data``.

Step 5 - Update your ``setup.py`` file
--------------------------------------

If you don’t have any compiled (e.g. C or Cython) extensions in your
package, you can replace your existing ``setup.py`` file with the
following:

.. code:: python

    #!/usr/bin/env python
    # Licensed under a 3-clause BSD style license - see LICENSE.rst

    # NOTE: The configuration for the package, including the name, version, and
    # other information are set in the setup.cfg file.

    import os
    import sys

    from setuptools import setup
    from extension_helpers import get_extensions

    # First provide helpful messages if contributors try and run legacy commands
    # for tests or docs.

    TEST_HELP = """
    Note: running tests is no longer done using 'python setup.py test'. Instead
    you will need to run:

        tox -e test

    If you don't already have tox installed, you can install it with:

        pip install tox

    If you only want to run part of the test suite, you can also use pytest
    directly with::

        pip install -e .[test]
        pytest

    For more information, see:

    http://docs.astropy.org/en/latest/development/testguide.html#running-tests
    """

    if 'test' in sys.argv:
        print(TEST_HELP)
        sys.exit(1)

    DOCS_HELP = """
    Note: building the documentation is no longer done using
    'python setup.py build_docs'. Instead you will need to run:

        tox -e build_docs

    If you don't already have tox installed, you can install it with:

        pip install tox

    You can also build the documentation with Sphinx directly using::

        pip install -e .[docs]
        cd docs
        make html

    For more information, see:

    http://docs.astropy.org/en/latest/install.html#builddocs
    """

    if 'build_docs' in sys.argv or 'build_sphinx' in sys.argv:
        print(DOCS_HELP)
        sys.exit(1)

    VERSION_TEMPLATE = """
    # Note that we need to fall back to the hard-coded version if either
    # setuptools_scm can't be imported or setuptools_scm can't determine the
    # version, so we catch the generic 'Exception'.
    try:
        from setuptools_scm import get_version
        version = get_version(root='..', relative_to=__file__)
    except Exception:
        version = '{version}'
    """.lstrip()

    setup(use_scm_version={'write_to': os.path.join('{{ cookiecutter.module_name }}', 'version.py'),
                        'write_to_template': VERSION_TEMPLATE},
        ext_modules=get_extensions())

Step 6: add a ``pyproject.toml`` file
-------------------------------------

The ``pyproject.toml`` file is used to declare dependencies needed to
run ``setup.py`` and build the package. If your package doesn’t have any
compiled extensions, the file should contain:

.. code:: toml

   [build-system]
   requires = ["setuptools",
               "wheel"]
   build-backend = 'setuptools.build_meta'

Step 7 - Handling C/Cython extensions
-------------------------------------

If your package has no compiled C/Cython extensions, you can skip this
step. Otherwise, if you have C or Cython extensions, you can either
define your extensions manually inside the ``setup.py`` file or make use
of the `extension-helpers <https://extension-helpers.readthedocs.io>`__
package to collect extensions in a similar way to astropy-helpers.

Step 7a - Defining extensions manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can define extensions manually as described
`here <https://oa-packaging-guide-preview.readthedocs.io/en/latest/extensions.html#defining-extensions-in-setup-py>`__.
If you do this, you can remove all ``setup_package.py`` files in your
package.

If you have Cython extensions or your extensions use the NumPy C API,
proceed to Step 7c, otherwise you can proceed to Step 8.

Step 7b - Using extension-helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the extension-helpers package to:

-  Automatically define extensions for Cython files
-  Pick up extensions declared in ``setup_package.py`` files, as
   described in the `extension-helpers
   documentation <https://extension-helpers.readthedocs.io/en/latest/>`__.

The latter works by looking through all the ``setup_package.py`` files
in your package and executing the ``get_extensions()`` functions, which
each should return a list of extensions. Check through your existing
``setup_package.py`` files (if any), and make sure that any
``astropy_helpers`` imports are changed to ``extension_helpers``.

Next, add:

.. code:: python

   from extension_helpers.setup_helpers import get_extensions

just under the following lines at the top of the ``setup.py`` file:

.. code:: python

   import sys
   from setuptools import setup

In addition, in the same file, change:

.. code:: python

   setup(use_scm_version={'write_to': os.path.join('my_package', 'version.py')})

to

.. code:: python

   setup(use_scm_version={'write_to': os.path.join('my_package', 'version.py')},
         ext_modules=get_extensions())

If you have Cython extensions or your extensions use the NumPy C API,
proceed to Step 7c, otherwise you can proceed to Step 8.

Step 7c - Cython and Numpy build-time dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your compiled extensions rely on the NumPy C API, you will need to
declare Numpy as a build-time dependency in ``pyproject.toml``. Note
that as described in `APE
17 <https://github.com/astropy/astropy-APEs/blob/master/APE17.rst#build-time-dependencies>`__,
you need to pin the build-time Numpy dependency to the **oldest**
supported Numpy version for each Python version. However, rather than
doing this manually, you can add the ``oldest-supported-numpy`` package
to your ``pyproject.toml`` file:

.. code:: toml

   [build-system]
   requires = ["setuptools",
               "wheel",
               "oldest-supported-numpy"]
   build-backend = 'setuptools.build_meta'

If you have Cython extensions, you will need to also add an entry for
Cython, pinning it to a recent version:

.. code:: toml

   [build-system]
   requires = ["setuptools",
               "wheel",
               "cython==0.29.14"]
   build-backend = 'setuptools.build_meta'

Whenever a new major Python version is released, you will likely need to
update this pinning to use the most recent Cython version available.

Step 8 - Using setuptools_scm
-----------------------------

The `setuptools_scm <https://pypi.org/project/setuptools-scm/>`__
package is now recommended to manage the version numbers for your
package. The way this works is that instead of setting the version
number manually in e.g. \ ``setup.cfg`` or elsewhere in your package,
the version number is based on git tags.

First, define ``setup_requires`` inside the ``[options]`` section of
your ``setup.cfg`` file::

   [options]
   ...
   setup_requires = setuptools_scm
   ...

Next, add ``setuptools_scm`` as a build-time dependency in the
``requires`` list of your ``pyproject.toml`` file:

.. code:: toml

   [build-system]
   requires = ["setuptools",
               "setuptools_scm",
               ...

Check your ``.gitignore`` and make sure that you have a line containing::

   my_package/version.py

Finally, edit your ``my_package/_astropy_init.py`` file and remove the
following lines:

.. code:: python

   try:
       from .version import githash as __githash__
   except ImportError:
       __githash__ = ''

and remove ``'__githash__'`` from the ``__all__`` list at the top of the
file.

The git hash is now contained in the version number, so this is no
longer needed.

Step 9 - Configuring pytest
---------------------------

To make sure that pytest works properly, you can set a few options in a
``[tool:pytest]`` section in your ``setup.cfg`` file::

   [tool:pytest]
   testpaths = "my_package" "docs"
   astropy_header = true
   doctest_plus = enabled
   text_file_format = rst
   addopts = --doctest-rst

For the ``testpaths`` line, make sure you replace ``my_package`` with
the name of your package.

The remaining options ensure that the output from pytest includes a
header that lists dependencies and system information, and also ensure
that the ``.rst`` files are picked up and tested by pytest.

Step 10 - Update ``MANIFEST.in``
--------------------------------

Edit your ``MANIFEST.in`` file to remove the following lines, if present
(and any other line related to ``astropy_helpers``) - those lines might
include any of the following::

   include ez_setup.py
   include ah_bootstrap.py

   # the next few stanzas are for astropy_helpers.  It's derived from the
   # astropy_helpers/MANIFEST.in, but requires additional includes for the actual
   # package directory and egg-info.

   include astropy_helpers/README.rst
   include astropy_helpers/CHANGES.rst
   include astropy_helpers/LICENSE.rst
   recursive-include astropy_helpers/licenses *

   include astropy_helpers/ez_setup.py
   include astropy_helpers/ah_bootstrap.py

   recursive-include astropy_helpers/astropy_helpers *.py *.pyx *.c *.h
   recursive-include astropy_helpers/astropy_helpers.egg-info *
   # include the sphinx stuff with "*" because there are css/html/rst/etc.
   recursive-include astropy_helpers/astropy_helpers/sphinx *

   prune astropy_helpers/build
   prune astropy_helpers/astropy_helpers/tests

Then add a new line near the top with the following::

   include pyproject.toml

Step 11 - Updating your documentation configuration
---------------------------------------------------

You will need to edit the ``docs/conf.py`` file to make sure it does not
use astropy-helpers. If you see a code block such as:

.. code:: python

    try:
       import astropy_helpers
    except ImportError:
       # Building from inside the docs/ directory?
       if os.path.basename(os.getcwd()) == 'docs':
           a_h_path = os.path.abspath(os.path.join('..', 'astropy_helpers'))
           if os.path.isdir(a_h_path):
               sys.path.insert(1, a_h_path)

   # Load all of the global Astropy configuration
   from astropy_helpers.sphinx.conf import *

   # Get configuration information from setup.cfg
   try:
       from ConfigParser import ConfigParser
   except ImportError:
       from configparser import ConfigParser

you should change it to:

.. code:: python

   try:
       from sphinx_astropy.conf.v1 import *  # noqa
   except ImportError:
       print('ERROR: the documentation requires the sphinx-astropy package to be installed')
       sys.exit(1)

   # Get configuration information from setup.cfg
   from configparser import ConfigParser
   conf = ConfigParser()

Find and replace any instances of ``package_name`` in the file with
``name``.

Step 12 - Setting up tox
------------------------

`tox <https://tox.readthedocs.io/en/latest/>`__ is a tool for automating
commands, which is well suited to e.g. running tests for your package or
building the documentation. One of the benefits of using tox is that it
will (by default) create a source distribution for your package and
install it into a virtual environment before running tests or building
docs, which means that it will be a good test of whether e.g. you have
declared the package data correctly.

Given the set-up described in the previous steps, you should be able to
create a ``tox.ini`` file at the root of your package with the following
content::

   [tox]
   envlist =
       py{36,37,38}-test{,-alldeps,-devdeps}
       build_docs
       codestyle
   requires =
       setuptools >= 30.3.0
       pip >= 19.3.1
   isolated_build = true
   module_name = my_package

   [testenv]
   passenv =
       HOME
       WINDIR
       LC_ALL
       LC_CTYPE
       CC
       CFLAGS
   changedir =
       test: .tmp/{envname}
       build_docs: docs
   description =
       test: run tests with pytest
       build_docs: invoke sphinx-build to build the HTML docs
       alldeps: run tests with all optional dependencies
       devdeps: run tests with numpy and astropy dev versions
   deps =
       astropylts: astropy==4.0rc2
       numpy116: numpy==1.16.*
       numpy117: numpy==1.17.*
       numpy118: numpy==1.18.*
       devdeps: git+https://github.com/numpy/numpy.git#egg=numpy
       devdeps: git+https://github.com/astropy/astropy.git#egg=astropy
   extras =
       test: test
       build_docs: docs
       alldeps: all
   commands =
       test: pytest --pyargs {[tox]module_name} {toxinidir}/docs --cov {[tox]module_name} --cov-config {toxinidir}/setup.cfg {posargs}
       build_docs: sphinx-build -W -b html . _build/html {posargs}

   [testenv:codestyle]
   skip_install = true
   description = check package code style
   deps = pycodestyle
   commands = pycodestyle {[tox]module_name}

Edit the ``module_name`` line in the ``[tox]`` section to specify your module
name. Once you have done this you should be able to do the following:

Run tests with minimal dependencies::

   tox -e test

Run tests with astropy LTS and Numpy 1.16::

   tox -e test-astropylts-numpy116

Run tests with all optional dependencies::

   tox -e test-alldeps

Run tests with minimal dependencies and the latest developer version of
numpy and astropy::

   tox -e test-devdeps

Build the documentation::

   tox -e build_docs

Run code style checks on your code::

   tox -e codestyle

The ``{posargs}`` corresponds to arguments passed to ``tox`` after a
``--`` separator - for example to make pytest verbose in a ``test``
environment, you can do::

   tox -e test -- -v

Step 13 - Updating your Continuous Integration
----------------------------------------------

This step will depend on what continuous integration services you use.
Broadly speaking, unless there are dependencies you need that can only
be installed with conda, you should no longer need to use ci-helpers.

The recommended approach is to use the tox file to set up the different
configurations you want to use, and to then keep the CI configuration as
simple as possible. For example, if you wanted to set up a Travis CI
file to run the tox environments defined in Step 10, you could use a
configuration such as:

.. code:: yaml

   language: c

   sudo: false

   env:
       global:
           - TOXENV=''
           - TOXARGS=''
           - TOXPOSARGS=''

   matrix:

       include:

           # Run the default test environment on
           # all major platforms

           - os: linux
             python: 3.8
             env: TOXENV='test'

           - os: osx
             env: PYTHON_VERSION=3.7 TOXENV='test'

           - os: windows
             env: PYTHON_VERSION=3.7 TOXENV='test'

           # Run the test-dev-all environment and pass the
           # --remote-data to demonstrate passing positional
           # arguments for pytest
           - os: linux
             python: 3.7
             env: TOXENV="test-all-dev"
                  TOXPOSARGS="--remote-data=astropy"

           # Build the docs
           - os: linux
             python: 3.7
             env: TOXENV="build_docs"

           # Run pycodestyle checks
           - os: linux
             python: 3.7
             env: TOXENV="pycodestyle"

   before_install:

       # We need a full clone to make sure setuptools_scm
       # works properly
       - git fetch --unshallow .
       - git fetch --depth=1000000

   install:

       - if [[ $TRAVIS_OS_NAME == osx || $TRAVIS_OS_NAME == windows ]]; then
           git clone git://github.com/astropy/ci-helpers.git;
           source ci-helpers/travis/setup_conda.sh;
         fi

       - pip install tox --upgrade

   script:
       - tox -e $TOXENV $TOXARGS -- $TOXPOSARGS

   after_success:
       - pip install codecov
       - codecov

Note that the above shouldn’t be used as-is - it just shows how one can
configure Travis to use tox, optionally using conda via ci-helpers to
set up Python on MacOS X and Windows, but you should adapt your existing
CI configuration rather than using the above.

Step 14 - Update ReadTheDocs configuration
------------------------------------------

With the set-up described in this migration guide, you should be able to
simplify the configuration for ReadTheDocs. This can be done via a
``readthedocs.yml`` or ``.readthedocs.yml`` file (the latter is
recommended). This file just needs to contain:

.. code:: yaml

   version: 2

   build:
     image: latest

   python:
     version: 3.7
     install:
       - method: pip
         path: .
         extra_requirements:
           - docs
           - all

If you don’t have the ``all`` extras_require defined, you can remove
that line.

If you don’t need to build non-HTML formats for the docs (e.g. epub),
you can also add the following line at the end of your
``.readthedocs.yml`` file:

.. code:: yaml

   formats: []

Step 15 - Coverage configuration
--------------------------------

Preivously, astropy-helpers expected the coverage configuration to
be located in ``my_package/tests/coveragerc``. This is now no longer
necessary, so you can now define the coverage configuration inside
the ``setup.cfg`` file, which should help reduce the number of files
to keep track of. Add the following to the bottom of your ``setup.cfg``::

    [coverage:run]
    omit =
        my_package/_{{ cookiecutter._parent_project }}_init*
        my_package/conftest.py
        my_package/*setup_package*
        my_package/tests/*
        my_package/*/tests/*
        my_package/extern/*
        my_package/version*
        */my_package/_{{ cookiecutter._parent_project }}_init*
        */my_package/conftest.py
        */my_package/*setup_package*
        */my_package/tests/*
        */my_package/*/tests/*
        */my_package/extern/*
        */my_package/version*

    [coverage:report]
    exclude_lines =
        # Have to re-enable the standard pragma
        pragma: no cover
        # Don't complain about packages we have installed
        except ImportError
        # Don't complain if tests don't hit assertions
        raise AssertionError
        raise NotImplementedError
        # Don't complain about script hooks
        def main\(.*\):
        # Ignore branches that don't pertain to this version of Python
        pragma: py{ignore_python_version}
        # Don't complain about IPython completion helper
        def _ipython_key_completions_

Make sure to replace ``my_package`` by your module name. If you had any
customizations in ``coveragerc`` you can include them here, but otherwise the
above should be sufficient.

Step 16 - conftest.py file updates
----------------------------------

For the header in your test runs to be correct with the latest versions of
astropy, you will need to make sure that you update your ``conftest.py``
file as described in the `pytest-astropy-header instructions
<https://github.com/astropy/pytest-astropy-header#migrating-from-the-astropy-header-plugin-to-pytest-astropy>`_.

Step 17 - Final cleanup
-----------------------

Once you’ve made the above changes, you should be able to remove the
following sections from your ``setup.cfg`` file:

-  ``[build_docs]``
-  ``[build_sphinx]``
-  ``[upload_docs]``

You should also add ``pip-wheel-metadata`` to your ``.gitignore`` file.

**Once you are done, if you would like us to help by reviewing your changes,
you can open a pull request to your package and mention @astrofrog or
@Cadair to ask for a review**
