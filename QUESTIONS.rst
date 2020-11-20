Package Setup Guide
===================

To use the package template run ``cookiecutter gh:astropy/package-template``,
once you have run this command you will be asked a series of questions. Below is
a description of each of the prompts.

1. ``package_name``: This is a human readable name for your package, like ``Astropy`` or ``SunPy``.
2. ``module_name``: This is the name of your python package i.e. ``astropy`` or ``sunpy``.
3. ``short_description``: This is a one sentence description of your package.
4. ``author_name``: The name or names of the authors.
5. ``author_email``: A contact email for the authors.
6. ``license``: The license of your package.
7. ``project_url``: Project website.
8. ``include_example_code``: This includes a set of example python files showing you how to use the package template. If you choose ``n`` then none of this will be included and you will have to populate the directory structure before you can import the package.
9. ``use_compiled_extensions``: Whether you plan to use compiled extensions in your package
10. ``edit_on_github_extension``: Set to ``True`` to enable the edit on GitHub sphinx extension.
11. ``github_project``: This is the GitHub identifier for the edit on GitHub extension and the changelog link extension.
12. ``use_gh_actions``: If ``'y'`` the template will include an example ``.github/workflows/tox-tests.yml`` file for the GitHub Actions CI service.
13. ``use_read_the_docs``: If ``'y'`` the ``read_the_docs.yml`` and ``.rtd-environment.yml`` files will be included for using conda on Read the Docs.
14. ``sphinx_theme``: The value of the ``html_theme`` variable in the sphinx configuration file.
15. ``required_dependencies``: Comma-separated list of required dependencies
16. ``optional_dependencies``: Comma-separated list of optional dependencies
17. ``minimum_python_version``: Version string of minimum supported Python version
18. ``private_project``: Whether this is a private project or not.
