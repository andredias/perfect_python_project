Perfect Python Project Template
===============================

This project template creates the basic structure for a Python project.
The article `How to Set up a Perfect Python Project <https://blog.pronus.io/en/posts/python/how-to-set-up-a-perfect-python-project/>`_ describes all the design decisions used here.


Features
--------

* Python 3.10+ (configurable)
* Poetry_ based dependency management
* Development tasks registered in a ``Makefile`` for easy access and management
* Custom Mercurial/Git hooks for ``pre-commit`` and ``pre-push`` events
* Linting based on ruff_, blue_, mypy_ and others
* Tests based on pytest_


Instructions
============

To instantiate the template into a new project, you'll need cookiecutter_.
The best way to use it just once is through pipx_:

.. code:: console

    $ pipx run cookiecutter gh:andredias/perfect_python_project

If you prefer, use can install it throught `pip` instead:

.. code:: console

    $ pip install --user cookiecutter

Next, run the following command:

.. code:: console

    $ cookiecutter gh:andredias/perfect_python_project

Answer a few questions:

.. code:: text

    author []: Fulano de Tal
    email []: fulano@email.com
    project_name [Project]: Project X
    project_slug [project_x]:
    python_version [3.10]:
    line_length [79]: 100
    Select version_control:
    1 - hg
    2 - git
    Choose from 1, 2 [1]: 1
    github_respository_url []:


That's it!


.. _blue: https://pypi.org/project/blue/
.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _mypy: http://mypy-lang.org/
.. _pipx: https://pypa.github.io/pipx/
.. _Poetry: https://python-poetry.org/
.. _pytest: https://pytest.org
.. _ruff: https://pypi.org/project/ruff/
