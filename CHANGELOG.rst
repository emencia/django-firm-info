.. _intro_history:

=======
History
=======


0.1.6 (2024-07-18)
------------------

New
~~~
*  Added complete FirmContact templatetag. [Samy Saad]


Changes
~~~~~~~
*  Enhanced code&tests quality. [Samy Saad]

  Added test for app_banner templatetag + test template
  Added test for firm_logos templatetag + test template
  Added test for social_sharing templatetag + test template
  Added Singleton tests
  Added post_delete and post_save signals tests

  Added SingletonManager for SocialSharing and Tracking models
  Added UniqueModelAdmin that reflect the behaviour of a singleton in admin

  Improved AppsBannerFactory
  Added SocialSharingFactory

  Added firm_logos serializer

Other
~~~~~
* [DOC] Improved documentation. [Samy Saad]


0.1.5 (2024-05-30)
------------------

Changes
~~~~~~~
*  [CHG] Added global context accessibility in template tags (Ticket #5289453) [Samy Saad]


Other
~~~~~
* [CHG] Removed dj4.0 and dj4.1 from tox tests [Samy Saad]
* [FIX] Added default autofield in settings [Samy Saad]
* [FIX] Fixed rtd build [Samy Saad]
* [DOC] Updated doc [Samy Saad]

0.1.4 (2023-09-21)
------------------

Changes
~~~~~~~
*  Modify firm_info tag (Ticket #4942172) [Samy Saad]

  - Add address parts as context variables in simple_tag
  - Rename `address` context variable to `fill_address`

Other
~~~~~
* [DOC] Add models, templatetags and serializers doc. [Samy Saad]


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
