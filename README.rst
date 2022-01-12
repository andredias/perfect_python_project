Cookiecutter Perfect Python Project
===================================

This template generator creates the basic structure for a Python project.

Features
--------

* Python 3.10+ (configurable)
* Poetry_ based dependency management
* Development tasks registered in a ``Makefile`` for easy access and management
* Mercurial/Git hooks for ``pre-commit`` and ``pre-push`` events
* Linting based on flake8_ (and plugins), blue_, mypy_ and isort_
* Asynchronous tests based on pytest_


Instructions
============

You must have pipx_ and cookiecutter_ installed:

.. code:: console

    $ pip install --user pipx
    $ pipx ensurepath
    $ pipx install cookiecutter


Usage
=====

You can use this template directly from its repository:

.. code:: console

    $ cookiecutter https://github.com/andredias/cookiecutter-perfect-python-project.git


You will be prompted to enter a bunch of project config values.
Then,
Cookiecutter will generate a project from the template,
using the values that you entered.

That's it!


.. _blue: https://pypi.org/project/blue/
.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _flake8: https://pypi.org/project/flake8/
.. _isort: https://pypi.org/project/isort/
.. _mypy: http://mypy-lang.org/
.. _pipx: https://pypa.github.io/pipx/
.. _Poetry: https://python-poetry.org/
.. _pytest: https://pytest.org
