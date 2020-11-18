.. _options:

Options during Setup
====================

To use the package template run ``cookiecutter gh:astropy/package-template``,
once you have run this command you will be asked a series of questions. Below is
a description of each of the prompts:

#. ``package_name``: This is a human readable name for your package, like ``Astropy`` or ``SunPy``.
#. ``module_name``: This is the name of your python package i.e. ``astropy`` or ``sunpy``.
#. ``short_description``: This is a one sentence description of your package.
#. ``author_name``: The name or names of the authors.
#. ``author_email``: A contact email for the authors.
#. ``license``: The license of your package.
#. ``project_url``: Project website.
#. ``include_example_code``: This includes a set of example python files showing you how to use the package template. If you choose ``n`` then none of this will be included and you will have to populate the directory structure before you can import the package.
#. ``use_compiled_extensions``: Whether you plan to use compiled extensions in your package
#. ``edit_on_github_extension``: Set to ``True`` to enable the edit on GitHub sphinx extension.
#. ``github_project``: This is the GitHub identifier for the edit on GitHub extension and the changelog link extension.
#. ``use_gh_actions``: If ``'y'`` the template will include an example ``.github/workflows/tox-tests.yml`` file for the GitHub Actions CI service.
#. ``use_read_the_docs``: If ``'y'`` the ``read_the_docs.yml`` and ``.rtd-environment.yml`` files will be included for using conda on Read the Docs.
#. ``sphinx_theme``: The value of the ``html_theme`` variable in the sphinx configuration file.
#. ``required_dependencies``: Comma-separated list of required dependencies
#. ``optional_dependencies``: Comma-separated list of optional dependencies
#. ``minimum_python_version``: Version string of minimum supported Python version

Once the project has been set up, any of the values can still be `manually
updated <http://docs.astropy.org/en/latest/development/astropy-package-template.html>`_.
In addition, further customization can also be carried out in the :ref:`next-steps`.
