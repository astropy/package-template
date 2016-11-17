{{ '*' * "%s Documentation"|format(cookiecutter.package_name)|length() }}
{{ cookiecutter.package_name }} Documentation
{{ '*' * "%s Documentation"|format(cookiecutter.package_name)|length() }}

This is the documentation for {{ cookiecutter.package_name }}.

Reference/API
=============

.. automodapi:: {{ cookiecutter.module_name }}
