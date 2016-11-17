# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This is an Astropy affiliated package.
"""

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._{{ cookiecutter._parent_project }}_init import *
# ----------------------------------------------------------------------------

{%- if '{{ cookiecutter.include_test_code }}' != 'y' -%}
# For egg_info test builds to pass, put package imports here.
# if not _ASTROPY_SETUP_:
#     from .example_mod import *
{%- else -%}
# For egg_info test builds to pass, put package imports here.
if not _ASTROPY_SETUP_:
    from .example_mod import *
{%- endif -%}
