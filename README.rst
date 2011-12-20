========================================
Affiliated Package Template Instructions
========================================

This package provides a template for packages that are affiliated with the
`astropy`_ project. This package design mirrors the layout of the main Astropy
repository, as well as reusing much of the helper code used to organize
Astropy.  The instructions below describe how to take this template and adjust
it for your particular affiliated package.

.. note::
    The instructions below assume you are using git for version control, as is
    used by the main Astropy repository.  If this is not the case, hopefully
    it will be clear from context what to do with your particular VCS.

* You may have already done this, if you are looking at this file locally, but
  if not, you will need to obtain a copy of the package template.  Assuming
  you have `git`_ installed, just do:

      git clone git://github.com/astropy/package-template.git newpackage

  This will download the latest version of the template from `github`_ and
  place it in a directory named ``newpackage``.

* Go into the directory you just created, and open the ``setup.py`` file
  with your favorite text editor.  In this file, do the following:

    1. Change the `PACKAGENAME` variable to whatever you decide your package
       should be named (for examples' sake, we will call it ``yourpkg``). By
       tradition/very strong suggestion, python package names should be all
       lower-case.
    2. Change the `DESCRIPTION` variable to a short (one or few sentence)
       description of your package.
    3. Define a longer description as a string in the `LONG_DESCRIPTION`
       variable.  You may want this to be the docstring of your package itself
       as Astropy does.  In this case, simple add ``import yourpkg`` somewhere
       above, and set ``LONG_DESCRIPTION = yourpkg.__doc__``.  Alternatively,
       you may omit the description by deleting the variable and deleting the
       line where it is used in the `setup()` function further down.
    4. Add your name and email address by changing the `AUTHOR` and
       `AUTHOR_EMAIL` variables.
    5. If your affiliated package has a website, change `URL` to point to that
       site.  Otherwise, you can leave it pointing to `astropy`_ or just
       delete it.
    6. Exit out of your text editor

* Now tell git to remember the changes you just made:

   git add setup.py
   git commit -m "adjusted setup.py for new project yourpkg"

* Decide what license you want to use to release your source code. If you
  don't care and/or are fine with the Astropy license, just edit the file
  ``licenses/LICENSE.rst`` with your name (or your collaboration's name) at
  the top as the licensees.  Otherwise, make sure to replace that file with
  whatever license you prefer, and update the `LICENSE` variable in
  ``setup.py`` to reflect your choice of license.  Again, tell git about your
  changes:

    git add licenses/LICENSE.rst
    git add setup.py  # if you changed the license and modified setup.py
    git commit -m "updated license for new project yourpkg"

* Take a moment to look over the ``packagename/example_mod.py``,
  ``packagename/test_example.py``, ``scripts/script_example``, and
  ``packagename/example.pyx`` files, as well as the
  ``packagename/example_subpkg`` directory. These are examples of a
  pure-python module, a test script, an example command-line script, a
  `Cython`_ module, and a sub-package, respectively. (`Cython`_ is a way to
  compile python-like code to C to make it run faster - see the project's web
  site for details). These are provided as examples of standard way to lay
  these out. Once you understand these, though, you'll want to delete them
  (and later replace with your own):

    git rm packagename/example_mod.py
    git rm scripts/script_example
    git rm packagename/example.pyx
    git rm packagename/test_example.py
    git rm -r packagename/example_subpkg
    git commit -m "removed examples from package template"

* Now rename the source code directory to match your project's name:

    git mv packagename yourpkg
    git commit -m "renamed template package source to new project yourpkg"

* Adjust the information in the documentation to match your new project by
  editing the ``docs/conf.py`` file.

  1. Change the ``PACKAGENAME`` and `project` variables to your project's name
     (note that `project` does not *need* to be exactly the same as the
     package name, but that's the normal convention).
  2. Update the `copyright` variable for the current year, and also your na,e
     or the name of your collaboration (e.g.,"2011, John Doe and the
     Amazing Package Collaboration.")
  3. If you ever expect to output your docs in LaTeX or as a man page, you'll
     also want to update the `latex_documents` and `man_pages` variables to
     reflect your project, name, and author list.

* Pass these changes on to git:

    git add docs/conf.py
    git commit -m "updated documentation for new project yourpkg"

* Update the names of the documentation files to match your package's name.
  First open ``docs/index.rst`` in a text editor and change the text
  "packagename/index.rst" to e.g., "yourpkg/index.rst".  Then do:

    git add docs/index.rst
    git mv docs/packagename docs/yourpkg
    git commit -m "Updated docs to reflect new project yourpkg"

* Edit this file (README.rst) and delete all of this content, and replace it
  with a short description of your affiliated package. Inform git:

    git add README.rst
    git commit -m "replaced README for new project yourpkg"

* You're now ready to start doing actual work on your affiliated package.  You
  will probably want to read over the developer guidelines of the Astropy
  documentation, and if you are hosting your code in GitHub, you might also
  want to read the `Github help <http://help.github.com/>`_ to ensure you know
  how to push your code to GitHub and some recommended workflows that work for
  the core Astropy project.

* Once you have started work on the affiliated package, you should register
  your package with the Astropy affiliated package registry. Instructions for
  doing this will be provided on the `astropy`_ website.

* Good luck with your code and your science!

.. _astropy: http://www.astropy.org/
.. _git: http://git-scm.com/
.. _github: http://github.com
.. _Cython: http://cython.org/
