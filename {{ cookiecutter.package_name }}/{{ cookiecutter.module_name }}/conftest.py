# This file is used to configure the behavior of pytest when using the Astropy
# test infrastructure.
import os

from astropy.version import version as astropy_version
from pytest_astropy_header.display import (PYTEST_HEADER_MODULES,
                                           TESTED_VERSIONS)

from astropy.tests.helper import enable_deprecations_as_exceptions

## Uncomment the following line to treat all DeprecationWarnings as
## exceptions. See API documentation for astropy.tests.helper module
## as the API might be different across several major releases.
# enable_deprecations_as_exceptions()


# Customize the following lines to add/remove entries from
# the list of packages for which version numbers are displayed when running
# the tests.
def pytest_configure(config):
    config.option.astropy_header = True
    PYTEST_HEADER_MODULES['Astropy'] = 'astropy'
    PYTEST_HEADER_MODULES.pop('h5py', None)

    # This is to figure out the package version, rather than
    # using Astropy's
    from .version import version, astropy_helpers_version

    packagename = os.path.basename(os.path.dirname(__file__))
    TESTED_VERSIONS[packagename] = version
    TESTED_VERSIONS['astropy_helpers'] = astropy_helpers_version
