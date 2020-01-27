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

.. _step0:

Step 0: Re-rendering the template
---------------------------------

In this guide, we will descibe the changes to make to the files in your package.
However, you may not currently have the latest version of all files from the
template, so this is also a good chance to make sure you are completely up to
date by re-rendering the cookiecutter template to a new folder::

    cookiecutter gh:astropy/package-template -o my_package_tmp

As you progress through this guide, you can then - if you wish - copy over the
newest version of the file, taking care to edit it if needed to match any
desired customizations you had previously. This will also be useful for any new
files which you can then just copy from the rendered template.

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

Copy the ``setup.py`` file you generated in :ref:`Step 0 <step0>` and replace your existing one
- it should be good to go as-is without any further customizations.

Step 6: add a ``pyproject.toml`` file
-------------------------------------

The ``pyproject.toml`` file is used to declare dependencies needed to run
``setup.py`` and build the package. Copy the ``pyproject.toml`` file you
generated in :ref:`Step 0 <step0>` and replace your existing one.

If your package doesn’t have any compiled extensions, the file should contain:

.. code:: toml

   [build-system]
   requires = ["setuptools",
               "setuptools_scm",
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
package, and you don't need to include extension-helpers in the
``pyproject.toml`` file.

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

Provided you indicated when you generated the template in :ref:`Step 0 <step0>`
that you wanted to use compiled extensions, you should be good to go. If not,
make sure you add:

.. code:: python

   from extension_helpers.setup_helpers import get_extensions

just under the following lines at the top of the ``setup.py`` file:

.. code:: python

   import sys
   from setuptools import setup

In addition, in the same file, add ``ext_modules=get_extensions()`` to the
call to ``setup.py``.

If you have Cython extensions or your extensions use the NumPy C API,
proceed to Step 7c, otherwise you can proceed to Step 8.

Step 7c - Cython and Numpy build-time dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your compiled extensions rely on the NumPy C API, you will need to
declare Numpy as a build-time dependency in ``pyproject.toml``. Note
that as described in `APE
17 <https://github.com/astropy/astropy-APEs/blob/master/APE17.rst#build-time-dependencies>`__,
you need to pin the build-time Numpy dependency to the **oldest**
supported Numpy version for each Python version. However, rather than doing this
manually, you can add the ``oldest-supported-numpy`` package to the build
dependencies in your ``pyproject.toml`` file. In addition if you have Cython
extensions, you will need to also add an entry for Cython, pinning it to a
recent version. Provided you indicated when you generated the template in :ref:`Step 0 <step0>`
that you wanted to use compiled extensions, you should be good to go as both
``oldest-supported-numpy`` and ``cython`` should be in the ``pyproject.toml``
file. In this case your ``pyproject.toml`` file will look like:

.. code:: toml

   [build-system]
   requires = ["setuptools",
               "setuptools_scm",
               "wheel",
               "extension-helpers",
               "oldest-supported-numpy",
               "cython==0.29.14"]
   build-backend = 'setuptools.build_meta'

Whenever a new major Python version is released, you will likely need to
update the Cython pinning to use the most recent Cython version available.

Step 8 - Using setuptools_scm
-----------------------------

The `setuptools_scm <https://pypi.org/project/setuptools-scm/>`__
package is now recommended to manage the version numbers for your
package. The way this works is that instead of setting the version
number manually in e.g. ``setup.cfg`` or elsewhere in your package,
the version number is based on git tags.

In Steps 5 and 6, we already added the required entry for
setuptools_scm to ``setup.py`` and ``pyproject.toml``.

In addition to these, we recommend that you define ``setup_requires`` inside the
``[options]`` section of your ``setup.cfg`` file::

   [options]
   ...
   setup_requires = setuptools_scm
   ...

This is not strictly necessary but will make it possible for ``python setup.py --version``
to work without having to install ``setuptools_scm`` manually.

Next, check your ``.gitignore`` and make sure that you have a line containing::

   my_package/version.py

Finally, copy over the ``_astropy_init.py`` file generated in :ref:`Step 0 <step0>`, or
alternatively edit your ``my_package/_astropy_init.py`` file and remove the
following lines:

.. code:: python

   try:
       from .version import githash as __githash__
   except ImportError:
       __githash__ = ''

and remove ``'__githash__'`` from the ``__all__`` list at the top of the
file. The git hash is now contained in the version number, so this is no
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

As a starting point, copy over the ``tox.ini`` file generated in :ref:`Step 0 <step0>`.
You can always then customize it if needed (although it should work out
of the box).

Once you have done this you should be able to do the following:

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

This step will depend on what continuous integration services you use. Broadly
speaking, unless there are dependencies you need that can only be installed with
conda, you should no longer need to use ci-helpers to install these. The
recommended approach is to use the tox file to set up the different
configurations you want to use, and to then keep the CI configuration as simple
as possible.

If you use Travis CI, a good place to start is the ``.travis.yml`` file
generated in :ref:`Step 0 <step0>`, and you can then see if any previous customizations you had
made need to be copied over. This file shows how one can configure Travis to use
tox, optionally using conda via ci-helpers to set up Python on MacOS X and
Windows.

Step 14 - Update ReadTheDocs configuration
------------------------------------------

With the set-up described in this migration guide, you should be able to
simplify the configuration for ReadTheDocs. This can be done via a
``readthedocs.yml`` or ``.readthedocs.yml`` file (the latter is recommended).
You should be able to copy over the ``.readthedocs.yml`` file created in :ref:`Step 0 <step0>`.
With this updated file, you should now be able to remove any pip requirements
file or conda yml file that were previously used by ``readthedocs.yml``.

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
astropy, you will need to make sure that you update your ``conftest.py`` file as
described in the `pytest-astropy-header instructions
<https://github.com/astropy/pytest-astropy-header#migrating-from-the-astropy-header-plugin-to-pytest-astropy>`_.
You can also just copy over the file created in :ref:`Step 0 <step0>` and add back any
customizations you had.

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
