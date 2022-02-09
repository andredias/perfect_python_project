Perfect Python Project
======================

This template generator creates the basic structure for a Python project.

Features
--------

* Python 3.10+ (configurable)
* Poetry_ based dependency management
* Development tasks registered in a ``Makefile`` for easy access and management
* Custom Mercurial/Git hooks for ``pre-commit`` and ``pre-push`` events
* Linting based on flake8_ (and plugins), blue_, mypy_, isort_ and others
* Tests based on pytest_


Instructions
============

You must have pipx_ installed:

.. code:: console

    $ pip install --user pipx
    $ pipx ensurepath


Usage
=====

You can use this template directly from its repository:

.. code:: console

    $ pipx run cookiecutter gh:andredias/perfect_python_project


You will be prompted to enter a bunch of project config values.
Then,
Cookiecutter will generate a project from the template in a directory relative to the current one.

.. note::

    You can define a different ouput directory by passing the ``--output-dir`` flag.

That's it!


.. _blue: https://pypi.org/project/blue/
.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _flake8: https://pypi.org/project/flake8/
.. _isort: https://pypi.org/project/isort/
.. _mypy: http://mypy-lang.org/
.. _pipx: https://pypa.github.io/pipx/
.. _Poetry: https://python-poetry.org/
.. _pytest: https://pytest.org
