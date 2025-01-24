.. _virtualenv: https://virtualenv.pypa.io
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _Sphinx: http://www.sphinx-doc.org
.. _tox: http://tox.readthedocs.io
.. _livereload: https://livereload.readthedocs.io
.. _twine: https://twine.readthedocs.io
.. _gitchangelog: https://github.com/vaab/gitchangelog 

.. _intro_development:

===========
Development
===========

Development requirements
************************

django-firm-info is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using `Flake8`_;
* `Sphinx`_ for documentation with enabled `Napoleon`_ extension (using
  *Google style*);
* `tox`_ to run tests on various environments;

Every requirements are available in package extra requirements in section
``dev``.

.. _install_development:

Install for development
***********************

First ensure you have `pip`_ and `virtualenv`_ packages installed then
type: ::

    git clone https://github.com/rage2000/django-firm-info.git
    cd django-firm-info
    make install

django-firm-info will be installed in editable mode from the
latest commit on master branch with some development tools.

Unittests
---------

Unittests are made to work on `Pytest`_, a shortcut in Makefile is available
to start them on your current development install: ::

    make tests

Tox
---

To ease development against multiple Python versions a tox configuration has
been added. You are strongly encouraged to use it to test your pull requests.

Just execute Tox: ::

    make tox

This will run tests for all configured Tox environments, it may takes some time so you
may use it only before releasing as a final check.

Documentation
-------------

You can easily build the documentation from one Makefile action: ::

    make docs

There is Makefile action ``livedocs`` to serve documentation and automatically
rebuild it when you change documentation files: ::

    make livedocs

Then go on ``http://localhost:8002/`` or your server machine IP with port 8002.

Note that you need to build the documentation at least once before using
``livedocs``.

Github Workflow and releasing
-----------------------------

We maintain two main branches: `dev` and `master`. The `dev` branch contains
all pre-release code, while the `master` branch holds the released code.

Development is conducted in secondary branches specific to individual features
or fixes. Once the code is ready for release, it is merged into `dev`.

To create a new release, follow these steps:

1. Update the `CHANGELOG.rst` file with the latest changes.
2. Update the version number in `setup.cfg` to reflect the next release version.
3. Create a tag corresponding to the next release version.
4. Merge the `dev` branch into `master`.

These steps can be streamlined using the `gitchangelog`_ tool (conf files are included in repo).

After the tag/master is pushed to GitHub, the CI/CD pipeline will handle the remaining
tasks and create automatically a github release and publish package on pypi.

CI/CD
-----

Three GitHub Actions scripts manage the CI/CD pipeline:

- **test_with_tox.yml**: Runs tests on each code push to the repository.
- **create_release_from_tag.yml**: Automatically creates a release when a tag
  is pushed, provided all tests pass. 
- **publish_to_pypi.yml**: Publishes the release to PyPI. Before publishing to
  the main PyPI, a test release is conducted on test.pypi.org.

Contribution
------------

* Every new feature or changed behavior must pass tests, Flake8 code quality
  and must be documented.
* Every feature or behavior must be compatible for all supported environment.
