FastAPI Project Template
========================

This project template creates the basic structure for a minimum FastAPI application.
It extends the `Perfect Python Project <https://github.com/andredias/perfect_python_project/tree/master>`_ template.

The template design and structure is described in these articles:

#. `Minimal Project in FastAPI <https://blog.pronus.xyz/en/posts/python/minimal-fastapi-project/>`_.
#. `Packaging and Distribution of the Minimal FastAPI Project <https://blog.pronus.xyz/en/posts/python/fastapi/packaging-and-distribution-of-the-minimal-fastapi-project/>`_



Features
--------

* FastAPI_ web framework
* Asynchronous database support based on `Encode Databases`_ and `SQLAlchemy Core`_
* Python 3.12+ (configurable)
* Poetry_ based dependency management
* Development tasks registered in a ``Makefile`` for easy access and management
* Custom Mercurial/Git hooks for ``pre-commit`` and ``pre-push`` events
* Linting based on ruff_, mypy_ and others
* Tests:

    * Tests based on pytest_
    * Asynchronous FastAPI tests based on HTTPX_ and alt-pytest-asyncio_
    * Correct `Lifespan Protocol <https://asgi.readthedocs.io/en/latest/specs/lifespan.html>`_ handling via asgi-lifespan_

* Logging based on Loguru_
* Configurable from a ``.env`` file when it is present while remaining configurable via the environment (python-dotenv_)
* Production ready distribution and deployment via Docker containers and Docker Compose


Instructions
============

To instantiate the template into a new project, you'll need cookiecutter_ (>=2.4.0).
The best way to use it just once is through pipx_:

.. code:: console

    $ pipx run cookiecutter gh:andredias/perfect_python_project -c fastapi-complete

If you prefer, use can install it throught `pip` instead:

.. code:: console

    $ pip install --user cookiecutter

Next, run the following command:

.. code:: console

    $ cookiecutter gh:andredias/perfect_python_project -c fastapi-complete

Answer a few questions:

.. code:: text

    author (): Fulano de Tal
    email (): fulano@email.com
    project_name (Project): Project X
    project_slug (project_x):
    python_version (3.12):
    line_length (100):
    Select version_control:
    1 - hg
    2 - git
    Choose from 1, 2 (1):
    worker_class (uvloop):

``worker_class`` refers to the worker class used by the ``hypercorn`` server.
The default is ``uvloop`` in ``posix`` systems and ``asyncio`` in ``nt`` systems.


That's it!


.. _alt-pytest-asyncio: https://pypi.org/project/alt-pytest-asyncio/
.. _asgi-lifespan: https://pypi.org/project/asgi-lifespan/
.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _Encode Databases: https://www.encode.io/databases/
.. _FastAPI: https://fastapi.tiangolo.com/
.. _HTTPX: https://www.python-httpx.org/
.. _Loguru: https://github.com/Delgan/loguru
.. _mypy: http://mypy-lang.org/
.. _pipx: https://pypa.github.io/pipx/
.. _Poetry: https://python-poetry.org/
.. _pytest: https://pytest.org
.. _python-dotenv: https://pypi.org/project/python-dotenv/
.. _ruff: https://pypi.org/project/ruff/
.. _SQLAlchemy Core: https://docs.sqlalchemy.org/en/latest/core/
