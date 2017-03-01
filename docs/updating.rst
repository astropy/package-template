Updating Your Package
=====================

Once you have setup your project there will come a time when some things in the
package template change, new versions of ``astropy_helpers`` or updates to the
infrastructure you want to utilise. Updating your package with these changes is
a balance between maintaining parity with the original template and customising
your project to your needs.


Using Cookiecutter to Update
----------------------------

It is possible to use the `cookiecutter` package to make it easier to update
your package with changes from the template. The basic workflow is to use
cookiecutter to create a clean version of the package template but with the
settings configured to your package and then pull the changes into your package.

.. note::

   As of cookiecutter 1.5 this is the best way of doing this. Work will continue
   to make this process easier, and possibly even automated.


1. **Render the template**: Putting in the same settings as the first time the
   template was rendered (or using ``--replay``) render the template to a
   temporary folder::

   $ cookiecutter [--replay] gh:astropy/package-template -o /tmp

2. **Make a new branch**::

   $ git checkout -b update_template

3. **Copy the template over your package**: (replacing 'packagename' with your package name)::

   $ cp -r /tmp/packagename ./

4. **Git diff the patch**::

   $ git diff


Using git Update
----------------

A pre-rendered version of the package template is automatically generated in the
`astropy/package-template <https://github.com/astropy/package-template/>`__
repository. This can be used as a git remote and changes pulled from it.

The downside of this approach is the branch is rendered using the default
settings, which means you are much more likely to get conflicts when you merge
this branch.

1. Add the Astropy package template repo as a git remote (if it is not already)::

   $ git remote add package-template

2. Pull from the remote::

   $ git remote update

3. Merge the branch::

   $ git merge package-template/rendered
