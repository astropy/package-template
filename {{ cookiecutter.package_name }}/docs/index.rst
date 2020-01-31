{{ '*' * "%s Documentation"|format(cookiecutter.package_name)|length() }}
{{ cookiecutter.package_name }} Documentation
{{ '*' * "%s Documentation"|format(cookiecutter.package_name)|length() }}

This is the documentation for {{ cookiecutter.package_name }}.
{% if cookiecutter.include_example_code == 'y' %}
.. toctree::
  :maxdepth: 2

  example_subpkg.rst
{% endif %}

Reference/API
=============

.. automodapi:: {{ cookiecutter.module_name }}
