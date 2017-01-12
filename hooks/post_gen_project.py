#!/usr/bin/env python

import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

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
        remove_file('{{ cookiecutter.module_name }}/example_c.pyx')
        remove_file('{{ cookiecutter.module_name }}/example_mod.py')
        remove_file('{{ cookiecutter.module_name }}/tests/test_example.py')

    if '{{ cookiecutter.initialize_git_repo }}' == 'y':
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
            new_repo.index.commit(
                "Initialize astropy_helpers at version {{ cookiecutter.astropy_helpers_version }}"
            )
