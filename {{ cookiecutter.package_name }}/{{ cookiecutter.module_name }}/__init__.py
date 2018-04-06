# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._{{ cookiecutter._parent_project }}_init import *
# ----------------------------------------------------------------------------

# Enforce Python version check during package import.
# This is the same check as the one at the top of setup.py
{% if cookiecutter.minimum_python_version %}
import sys
class UnsupportedPythonError(Exception):
    pass
if sys.version_info < tuple((int(val) for val in {{ cookiecutter.minimum_python_version }}.split('.'))):
    raise UnsupportedPythonError("{{ cookiecutter.module_name }} does not support Python < {}".format({{ cookiecutter.minimum_python_version }}))
{% endif %}

if not _ASTROPY_SETUP_:
    # For egg_info test builds to pass, put package imports here.
{% if cookiecutter.include_example_code != 'y' %}
    pass
{% else %}
    from .example_mod import *
{% endif %}
