#!/usr/bin/env python

import os
import shutil
import urllib.request


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


def process_licence(licence_name):
    if licence_name in license_files:
        shutil.copyfile(os.path.join(PROJECT_DIRECTORY, 'licenses', license_files[licence_name]),
                        os.path.join(PROJECT_DIRECTORY, 'licenses', 'LICENSE.rst'))

    if licence_name != "Other":
        for licence_file in license_files.values():
            os.remove(os.path.join(PROJECT_DIRECTORY, 'licenses', licence_file))


if __name__ == '__main__':

    process_licence('{{ cookiecutter.license }}')

    if '{{ cookiecutter.use_travis_ci }}' != 'y':
        remove_file('.travis.yml')

    if '{{ cookiecutter.use_appveyor_ci }}' != 'y':
        remove_file('appveyor.yml')

    if '{{ cookiecutter.use_read_the_docs }}' != 'y':
        remove_file('.rtd-environment.yml')
        remove_file('readthedocs.yml')

    if '{{ cookiecutter.include_cextern_folder }}' != 'y':
        remove_dir("cextern")

    if '{{ cookiecutter.include_example_code }}' != 'y':
        remove_dir('{{ cookiecutter.module_name }}/example_subpkg/')
        remove_file('{{ cookiecutter.module_name }}/example_mod.py')
        remove_file('{{ cookiecutter.module_name }}/tests/test_example.py')

    if '{{ cookiecutter.include_example_cython_code }}' != 'y':
        remove_file('{{ cookiecutter.module_name }}/example_c.pyx')

    if '{{ cookiecutter.initialize_git_repo }}' == 'y':
        try:
            from git import Repo

            new_repo = Repo.init(PROJECT_DIRECTORY)
            new_repo.git.add('.')
            new_repo.index.commit(
                "Creation of {{ cookiecutter.package_name }} from astropy package template"
            )

            if '{{ cookiecutter.astropy_helpers_version }}':
                Repo.create_submodule(
                    new_repo, "astropy_helpers", "astropy_helpers",
                    "https://github.com/astropy/astropy-helpers.git",
                    "{{ cookiecutter.astropy_helpers_version }}")
                new_repo.submodules[0].update()
                copy_file('astropy_helpers/ah_bootstrap.py', 'ah_bootstrap.py')
                new_repo.git.add('ah_bootstrap.py')
                new_repo.index.commit(
                    "Initialize astropy_helpers at version {{ cookiecutter.astropy_helpers_version }}"
                )

        except ImportError:
            print(
                "gitpython is not installed so the repository will not be initialised "
                "and astropy_helpers not downloaded.")

    else:
        with urllib.request.urlopen(
                'https://raw.githubusercontent.com/astropy/astropy-helpers/'
                '{{ cookiecutter.astropy_helpers_version }}/ah_bootstrap.py') as ah:
            with open('ah_bootstrap.py', mode='wb') as ah_file:
                shutil.copyfileobj(ah, ah_file)
