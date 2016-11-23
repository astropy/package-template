Data directory
==============

This directory contains data files included with the affiliated package source
code distribution. Note that this is intended only for relatively small files
- large files should be externally hosted and downloaded as needed.

The ``test`` directory can be used to store files needed for tests, the path to
the directory is generated programatically in ``data/test/__init__.py`` so the
correct path to the data can always be obtained with the ``from
packagename.data.test import rootdir`` import.

