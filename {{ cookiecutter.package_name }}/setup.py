#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# Note: This file needs to be Python 2 / <3.6 compatible, so that the nice
# "This package only supports Python 3.x+" error prints without syntax errors etc.

import glob
import os
import sys

from distutils.version import LooseVersion

# We require setuptools 30.3.0 or later for the configuration in setup.cfg to
# work properly.
import setuptools
if LooseVersion(setuptools.__version__) < LooseVersion('30.3.0'):
    sys.stderr.write("ERROR: {{ cookiecutter.module_name }} requires setuptools 30.3.0 or later "
                     "(found {0})".format(setuptools.__version__))
    sys.exit(1)

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

# Get some values from the setup.cfg
conf = ConfigParser()
conf.read(['setup.cfg'])
metadata = dict(conf.items('metadata'))

__minimum_python_version__ = metadata["minimum_python_version"]

import ah_bootstrap
from setuptools import setup
{% if cookiecutter.minimum_python_version.startswith("2") %}
# A dirty hack to get around some early import/configurations ambiguities
if sys.version_info[0] >= 3:
    import builtins
else:
    import __builtin__ as builtins
{%- else %}
import builtins
{%- endif %}
builtins._ASTROPY_SETUP_ = True

from astropy_helpers.setup_helpers import (register_commands, get_debug_option,
                                           get_package_info)
from astropy_helpers.git_helpers import get_git_devstr
from astropy_helpers.version_helpers import generate_version_py

PACKAGENAME = metadata['name']

# Store the package name in a built-in variable so it's easy
# to get from other parts of the setup infrastructure
builtins._ASTROPY_PACKAGE_NAME_ = PACKAGENAME

# VERSION should be PEP440 compatible (http://www.python.org/dev/peps/pep-0440)
VERSION = metadata['version']

# Indicates if this version is a release version
RELEASE = 'dev' not in VERSION

if not RELEASE:
    VERSION += get_git_devstr(False)

# Populate the dict of setup command overrides; this should be done before
# invoking any other functionality from distutils since it can potentially
# modify distutils' behavior.
cmdclassd = register_commands(PACKAGENAME, VERSION, RELEASE)

# Freeze build information in version.py
generate_version_py(PACKAGENAME, VERSION, RELEASE,
                    get_debug_option(PACKAGENAME))

# Treat everything in scripts except README* as a script to be installed
scripts = [fname for fname in glob.glob(os.path.join('scripts', '*'))
           if not os.path.basename(fname).startswith('README')]


# Get configuration information from all of the various subpackages.
# See the docstring for setup_helpers.update_package_files for more
# details.
package_info = get_package_info()

# Note that requires and provides should not be included in the call to
# ``setup``, since these are now deprecated. See this link for more details:
# https://groups.google.com/forum/#!topic/astropy-dev/urYO8ckB2uM

setup(scripts=scripts,
      cmdclass=cmdclassd,
      python_requires='>={}'.format(__minimum_python_version__),
      **package_info
)
