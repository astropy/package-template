.. _{{ cookiecutter.package_name }}-credits:

*******************
Authors and Credits
*******************

Main author:

{{ cookiecutter.author_name }} (`{{ cookiecutter.github_project }} <{{ cookiecutter.github_project }}>`_)


Core Package Contributors
=========================

|Contributors|

All contributors (alphabetical last name):

{% for req in cookiecutter.author_name.split(',') %}
    * {{ req.strip() }}
{% endfor %}


Credits
=======

{% if cookiecutter._parent_project == "astropy" %}
* Astropy: `package template <https://github.com/astropy/package-template>`_
{% else %}
* {{ cookiecutter._parent_project }}: `package template <https://github.com/{{ cookiecutter._parent_project }}/package-template>`_
* Astropy: `astropy package template <https://github.com/astropy/package-template>`_
{% endif %}


..
  RST SUBSTITUTIONS

.. BADGES

.. |Contributors| image:: https://img.shields.io/github/contributors/{{ cookiecutter.github_project }}?style=flat
   :alt: GitHub contributors

