from __future__ import absolute_import

import os
import glob

import packagename

__all__ = ["rootdir", "file_list"]

# rootdir is the path to this folder
rootdir = os.path.join(os.path.dirname(sunpy.__file__), "data", "test")

# List of all files in the test directory excluding python files
file_list = glob.glob(os.path.join(rootdir, '*.[!p]*'))
