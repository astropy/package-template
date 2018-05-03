{{ cookiecutter.short_description }}
{{ '-' * cookiecutter.short_description|length }}

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

{{ cookiecutter.long_description|wordwrap(break_long_words=False) }}


License
-------

This project is Copyright (c) {{ cookiecutter.author_name }} and licensed under
the terms of the {{ cookiecutter.license }} license. This package is based upon
the `Astropy package template <https://github.com/astropy/package-template>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.
