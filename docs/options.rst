.. _options:

Options during Setup
====================

To use the package template run ``cookiecutter gh:astropy/package-template``,
once you have run this command you will be asked a series of questions. Below is
a description of each of the prompts:

#. ``package_name``: This is a human readable name for your package, like ``Astropy`` or ``SunPy``.
#. ``module_name``: This is the name of your python package i.e. ``astropy`` or ``sunpy``.
#. ``short_description``: This is a one sentence description of your package.
#. ``long_description``: This is a multi-line description of your package.
#. ``author_name``: The name or names of the authors.
#. ``author_email``: A contact email for the authors.
#. ``license``: The license of your package.
#. ``project_url``: Project website.
#. ``project_version``: The version number for the package.
#. ``include_example_code``: This includes a set of example python files showing you how to use the package template. If you choose ``n`` then none of this will be included and you will have to populate the directory structure before you can import the package.
#. ``include_example_cython_code``: This includes a set of example Cython code, which demonstrates how to add compiled code to the package.
#. ``include_cextern_folder``: The cextern folder should be used if you are including non-python C code.
#. ``edit_on_github_extension``: Set to ``True`` to enable the edit on GitHub sphinx extension.
#. ``github_project``: This is the GitHub identifier for the edit on GitHub extension and the changelog link extension.
#. ``use_travis_ci``: If ``'y'`` the template will include an example ``.travis.yml`` file for the Travis CI service.
#. ``use_appveyor_ci``: If ``'y'`` the template will include an example ``appveyor.yml`` file for the Appveyor CI service.
#. ``use_read_the_docs``: If ``'y'`` the ``read_the_docs.yml`` and ``.rtd-environment.yml`` files will be included for using conda on Read the Docs.
#. ``sphinx_theme``: The value of the ``html_theme`` variable in the sphinx configuration file.
#. ``initialize_git_repo``: If `gitpython <https://gitpython.readthedocs.io/en/stable/>`_ is installed this option will turn the rendered package into a git repository and add and initilize the ``astropy_helpers`` submodule.
#. ``astropy_helpers_version``: The version number of the ``astropy_helpers`` submodule to be used, only used if ``initialize_git_repo`` is true.

Once the project has been set up, any of the values can still be `manually
updated <http://docs.astropy.org/en/latest/development/astropy-package-template.html>`_.
In addition, further customization can also be carreid out in the :ref:`next-steps`.
