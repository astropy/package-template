#!/usr/bin/env python

import os
import shutil


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


def copy_file(original_filepath, new_filepath):
    shutil.copyfile(os.path.join(PROJECT_DIRECTORY, original_filepath),
                    os.path.join(PROJECT_DIRECTORY, new_filepath))


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

license_files = {"BSD 3-Clause": 'BSD3.rst',
                 "GNU GPL v3+": 'GPLv3.rst',
                 "Apache Software Licence 2.0": 'APACHE2.rst',
                 "BSD 2-Clause": 'BSD2.rst'}


def process_license(license_name):
    if license_name in license_files:
        shutil.copyfile(os.path.join(PROJECT_DIRECTORY, 'licenses', license_files[license_name]),
                        os.path.join(PROJECT_DIRECTORY, 'licenses', 'LICENSE.rst'))

    if license_name != "Other":
        for license_file in license_files.values():
            os.remove(os.path.join(PROJECT_DIRECTORY, 'licenses', license_file))


if __name__ == '__main__':

    process_license('{{ cookiecutter.license }}')

    if '{{ cookiecutter.use_gh_actions }}' != 'y':
        remove_dir('.github')

    if '{{ cookiecutter.use_read_the_docs }}' != 'y':
        remove_file('.rtd-environment.yml')
        remove_file('readthedocs.yml')

    if '{{ cookiecutter.include_example_code }}' != 'y':
        remove_dir('{{ cookiecutter.module_name }}/example_subpkg/')
        remove_file('{{ cookiecutter.module_name }}/example_mod.py')
        remove_file('{{ cookiecutter.module_name }}/tests/test_example.py')

    if '{{ cookiecutter.use_compiled_extensions }}' != 'y' or '{{ cookiecutter.include_example_code }}' != 'y':
        remove_file('{{ cookiecutter.module_name }}/example_c.pyx')
