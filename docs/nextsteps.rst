.. _next-steps:

Next Steps
==========

Setting Up Continuous Integration
---------------------------------

Once you have rendered your package and set it up on `GitHub
<https://github.com>`__ you may wish to enable Travis CI, Appveyor and Read the
Docs (configuration for these services is included in the template, but you
could utilise others).

Travis CI
#########

You should register your package on https://travis-ci.org and modify the
``.travis.yml`` file to your needs. The default ``.travis.yml`` file contains a
large number of builds, against various versions of Python and Astropy and
numpy, you should choose the ones relevant to your project. Full documentation
of the ``.travis.yml`` file can be found on the
`Travis CI <https://docs.travis-ci.com/user/for-beginners/>`__ website.

Continuous Integration services like Travis CI, continuously test your package
for each commit, even pull requests against your main repository will be
automatically tested, so that you notice when something breaks. For further
information see `here
<https://github.com/astropy/astropy/wiki/Continuous-Integration>`__ and for
lots of example ``.travis.yml`` build configurations see `here
<https://github.com/astropy/astropy/wiki/travis-ci-test-status>`__. Generally
you should aim to always have your ``master`` branch work with the latest stable
as well as the latest development version of astropy (i.e. the astropy git
master branch) and the same versions of python and numpy supported by astropy.
The template ``.travis.yml`` covers those versions; in some circumstances you
may need to limit the versions your package covers.

Appveyor
########

Appveyor provides testing on the Windows platform, if you want to enable this
you should register and enable your project at https://www.appveyor.com/. The
appveyor build is controlled by the ``appveyor.yml`` file included in the
template (by default).

Coveralls
#########

Coveralls is a web interface to monitoring what lines of code in your project
are executed by your test suite.

If you register your package with coveralls.io, you will need to uncomment the
coveralls line in the ``.travis.yml`` file to enable upload of your coverage
statistics to coveralls.


Read the Docs
#############

If you want the documentation for your project to be hosted by `Read the Docs
<https://readthedocs.org>`_, then you need to setup an account there. The
following entries in "Advanced Settings" for your package on `Read the Docs
<https://readthedocs.org>`_ should work:

- Activate ``Install your project inside a virtualenv using setup.py install``
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
