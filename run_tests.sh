#!/bin/bash -xe

# Go to project folder
cd $1

# Run package tests and docs
python setup.py egg_info
python setup.py build
python setup.py build_docs
python setup.py test
python setup.py check --restructuredtext

# Make sure the Travis file is valid
travis lint
