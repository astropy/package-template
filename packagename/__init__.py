# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *
# ----------------------------------------------------------------------------

# Enforce Python version check during package import.
# This is the same check as the one at the top of setup.py


if not _ASTROPY_SETUP_:
    # For egg_info test builds to pass, put package imports here.

    from .example_mod import *

