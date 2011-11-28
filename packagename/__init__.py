from __future__ import division
from .tests.helper import run_tests as test
from example import fib


try:
    from .version import version as __version__
except ImportError:
    # TODO: Issue a warning...
    __version__ = ''
