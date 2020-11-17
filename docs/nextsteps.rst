.. _next-steps:

Next Steps
==========

Once you have rendered your package and set it up on `GitHub
<https://github.com>`__ you may wish to enable `Travis CI
<https://travis-ci.org>`_ and
`Read the Docs <https://readthedocs.org/>`_.  Configuration for these services
is included in the template, and while their use is optional, it is
recommended.

Setting Up Continuous Integration
---------------------------------

`Continuous Integration
<https://github.com/astropy/astropy/wiki/Continuous-Integration>`__ (CI)
services continuously test your package
for each commit. Every pull request against your main repository will be
automatically tested and failing tests will be flagged by these services.

Github Actions
##############

Github now provides an integrated CI service called `Github Actions <https://docs.github.com/en/free-pro-team@latest/actions>`__.
The default workflows in ``.github/workflows`` show how to set up perform integration testing
upon every push or pull request, ``ci_tests.yml``, and how to run scheduled tests via cron, ``ci_cron_weekly.yml``.
The default ``ci_tests.yml`` file contains a large number of builds against various versions of Python, astropy, and
numpy, and you should choose the ones relevant to your project. Generally you should aim to always have your ``master`` branch
work with the latest stable and latest development version of astropy (i.e. the
astropy git master branch) and the same versions of python and numpy supported
by astropy.  The template ``ci_tests.yml`` covers those versions; in some
circumstances you may need to limit the versions your package covers.

Codecov
#######

Codecov is a web interface to monitoring what lines of code in your project
are executed by your test suite.

If you register your package with `codecov.io <https://codecov.io/>`_, you
will need to uncomment the codecov section in the ``ci_tests.yml`` file under
``.github/workflows`` to enable upload of your coverage statistics to codecov.

Read the Docs
#############

In addition to testing the code, it is often useful to build documentation
continuously as the code is developed. Read the Docs is a web site that
provides exactly this service.  If you want the documentation for your
project to be hosted by `Read the Docs
<https://readthedocs.org>`__, then you need to setup an account there. The
following entries in "Advanced Settings" for your package on `Read the Docs
<https://readthedocs.org>`__ should work:

- Select ``Install your project inside a virtualenv using setup.py install``
- Edit ``.rtd-environment.yml`` with your package requirements (this file is
  used by conda on RTD to install the requirements for your package).
- Activate ``Give the virtual environment access to the global site-packages
  dir.``

All other settings can stay on their default value.

Customizing the package
-----------------------

Once you have run cookiecutter you can edit the files in the folder to further
customize your package. This section of the documentation lists some ways you
might want to do this.

Customizing the package metadata
################################

All of the metadata about the package (name, version, keywords, etc.) are
defined in the ``setup.cfg`` file. This is described in detail in the
`setuptools documentation <https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files>`_.

Customizing the documentation CSS
#################################

As described in the documentation configuration file (`template/docs/conf.py
<https://github.com/astropy/package-template/blob/master/docs/conf.py#L95>`_),
the documentation uses a custom theme based on `bootstrap
<http://getbootstrap.com/css/>`_. You can swap out this theme by editing the
configuration file. You can also tweak aspects of the documentation theme by
creating a custom CSS file in your package documentation.

To do this, create a new CSS file in ``<packagename>/_static/`` -- let's call it
``<packagename>.css``::

    cd <packagename>/_static/
    touch <packagename>.css

We're going to set the HTML style to this new ``<packagename>.css`` stylesheet,
so we need to import the original ``bootstrap-astropy`` style before we start
modifying entries. To the first line of your ``<packagename>.css`` file, import
the default style. We can add any custom CSS below the import. For example, to
hide the Astropy logo and Astropy link from your project's documentation menu
bar:

.. code-block:: css

    @import url("bootstrap-astropy.css");

    div.topbar a.brand {
        background: none;
        background-image: none;
    }

    div.topbar ul li a.homelink {
        background: none;
        background-image: none;
    }

We now have to include the ``<packagename>.css`` in the documentation, and tell
Sphinx to use the new style. To do this, edit your
``<packagename>/docs/conf.py`` file and add the lines::

    # Static files to copy after template files
    html_static_path = ['_static']
    html_style = '<packagename>.css'
