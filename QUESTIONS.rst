Package Setup Guide
===================

To use the package template run ``cookiecutter gh:astropy/package-template``,
once you have run this command you will be asked a series of questions. Below is
a description of each of the prompts.

1. ``package_name``: This is a human readable name for your package, like 'Astropy' or 'SunPy'.
2. ``module_name``: This is the name of your python package i.e. 'astropy' or 'sunpy'.
3. ``short_description``: This is a one sentence description of your package.
4. ``long_description``: This is a multi-line description of your package.
5. ``author_name``: The name or names of the authors.
6. ``author_email``: A contact email for the authors.
7. ``license``: The license of your project.
8. ``project_url``: Project website.
9. ``include_example_code``: This includes a set of example python and cython files showing you how to use the package template. If you choose 'n' then none of this will be included and you will have to populate the directory structure before you can import the package.
10. ``include_cextern_folder``: The cextern folder should be used if you are including non-python C code.
11. ``edit_on_github_extension``: Set to "True" to enable the edit on GitHub sphinx extension.
12. ``github_project``: This is the GitHub identifier for the edit on GitHub extension and the changelog link extension.
13. ``project_version``: The current version number of your project.
14. ``use_travis_ci``: If 'y' the template will include an example ``.travis.yml`` file for the Travis CI service.
15. ``use_appveyor_ci``: If 'y' the template will include an example ``appveyor.yml`` file for the Appveyor CI service.
16. ``use_read_the_docs``: If 'y' the ``read_the_docs.yml`` and ``.rtd-environment.yml`` files will be included for using conda on Read the Docs.
17. ``sphinx_theme``: The value of the ``html_theme`` variable in the sphinx configuration file.
18. ``__minimum_python_version__``: Version string of minimum supported Python version. For example, "3.5" or "2.7". Leave as "" to skip this check.
