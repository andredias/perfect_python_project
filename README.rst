FastAPI Minimum Project Template
================================

This project template creates the basic structure for a minimum FastAPI application.
It is built from the `Perfect Python Project <https://github.com/andredias/perfect_python_project>`_ template.


Features
--------

* FastAPI_ web framework
* Python 3.10+ (configurable)
* Poetry_ based dependency management
* Development tasks registered in a ``Makefile`` for easy access and management
* Custom Mercurial/Git hooks for ``pre-commit`` and ``pre-push`` events
* Linting based on flake8_ (and plugins), blue_, mypy_, isort_ and others
* Tests:

    * Tests based on pytest_
    * Asynchronous FastAPI tests based on HTTPX_ and alt-pytest-asyncio_
    * Correct `Lifespan Protocol <https://asgi.readthedocs.io/en/latest/specs/lifespan.html>`_ handling via asgi-lifespan_

* Logging based on Loguru_
* Configurable from a ``.env`` file when it is present while remaining configurable via the environment (python-dotenv_)


Instructions
============

Install cookiecutter_ using pipx_:

.. code:: console

    $ pipx install cookiecutter

Or, if you prefer, use `pip` instead:

.. code:: console

    $ pip install --user cookiecutter

Next, run the following command:

.. code:: console

    $ cookiecutter gh:andredias/perfect_python_project -c fastapi-minimum

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


.. _alt-pytest-asyncio: https://pypi.org/project/alt-pytest-asyncio/
.. _asgi-lifespan: https://pypi.org/project/asgi-lifespan/
.. _blue: https://pypi.org/project/blue/
.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _FastAPI: https://fastapi.tiangolo.com/
.. _flake8: https://pypi.org/project/flake8/
.. _HTTPX: https://www.python-httpx.org/
.. _isort: https://pypi.org/project/isort/
.. _Loguru: https://github.com/Delgan/loguru
.. _mypy: http://mypy-lang.org/
.. _pipx: https://pypa.github.io/pipx/
.. _Poetry: https://python-poetry.org/
.. _pytest: https://pytest.org
.. _python-dotenv: https://pypi.org/project/python-dotenv/
