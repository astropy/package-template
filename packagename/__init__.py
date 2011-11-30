from __future__ import division
from example import fib


try:
    from .version import version as __version__
except ImportError:
    # TODO: Issue a warning...
    __version__ = ''

# set up the test command
from . import __path__
from astropy.tests.helper import TestRunner
_test_runner = TestRunner(__path__[0])
del TestRunner
test = _test_runner.run_tests