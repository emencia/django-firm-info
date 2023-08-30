.. _intro_history:

=======
History
=======

0.1.3 (2023-08-30)
------------------

Fix
~~~
*  Typo in publish_to_pypi.yml workflow. [Lafaye Philippe]


0.1.2 (2023-08-30)
------------------

New
~~~
*  Create github release when new tag that match [0-9]+.[0-9]+.[0-9]+ name. [Lafaye Philippe]


Changes
~~~~~~~
*  publish on pypi when release was created. [Lafaye Philippe]


0.1.1 (2023-08-30)
------------------

New
~~~
*  Add github workflow for running publish to pypi. [Lafaye Philippe]

*  Add CodeQL workflow for testing. [Lafaye Philippe]

*  Add github workflow for running tox. [Lafaye Philippe]


Changes
~~~~~~~
*  Run publish_to_pypi workflow only is Test workflow is completed. [Lafaye Philippe]

*  Rename test workflow. [Lafaye Philippe]

*  Add missing __init__ file. [Lafaye Philippe]


Fix
~~~
*  Update django settings for doc building. [Lafaye Philippe]

*  Wrong main branch for publish to pypi workflow. [Lafaye Philippe]


0.1.0 - Unreleased
------------------

* First commit.
