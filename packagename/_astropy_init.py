# Licensed under a 3-clause BSD style license - see LICENSE.rst

__all__ = ['__version__', '__githash__', 'test']

# this indicates whether or not we are in the package's setup.py
try:
    _ASTROPY_SETUP_
except NameError:
    from sys import version_info
    if version_info[0] >= 3:
        import builtins
    else:
        import __builtin__ as builtins
    builtins._ASTROPY_SETUP_ = False

try:
    from .version import version as __version__
except ImportError:
    __version__ = ''
try:
    from .version import githash as __githash__
except ImportError:
    __githash__ = ''

import os
from astropy.tests.runner import TestRunner
test = TestRunner.make_test_runner_in(os.path.dirname(__file__))

if not _ASTROPY_SETUP_:
    import os
    from warnings import warn
    from astropy import config

    # add these here so we only need to cleanup the namespace at the end
    config_dir = None

    if not os.environ.get('ASTROPY_SKIP_CONFIG_UPDATE', False):
        config_dir = os.path.dirname(__file__)
        config_template = os.path.join(config_dir, __package__ + ".cfg")
        if os.path.isfile(config_template):
            try:
                config.configuration.update_default_config(
                    __package__, config_dir, version=__version__)
            except TypeError as orig_error:
                try:
                    config.configuration.update_default_config(
                        __package__, config_dir)
                except config.configuration.ConfigurationDefaultMissingError as e:
                    wmsg = (e.args[0] + " Cannot install default profile. If you are "
                            "importing from source, this is expected.")
                    warn(config.configuration.ConfigurationDefaultMissingWarning(wmsg))
                    del e
                except:
                    raise orig_error
