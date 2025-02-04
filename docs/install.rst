.. _djangocms-text: https://github.com/django-cms/djangocms-text
.. _djangocms-text-ckeditor: https://github.com/django-cms/djangocms-text-ckeditor

.. _intro_install:

=======
Install
=======

Install package in your environment : ::

    pip install django-firm-info

For development install see :ref:`install_development`, this is also a good way to
quick start a demonstration since development install have a demonstration site ready
to run.

Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "sorl.thumbnail",
        "smart_media",
        "firm_info",
    )

Then import the default settings: ::

    from smart_media.settings import *
    from firm_info.defaults import *

You may not import these defaults but you will have to define them all in your project
settings.

.. Note::

    Instead, if your project use
    `django-configuration <https://django-configurations.readthedocs.io/en/stable/>`_,
    your settings class can inherits from
    ``from firm_info.contrib.django_configuration import FirmInfosDefaultSettings``
    and the settings class from SmartMedia see
    `SmartMedia configuration documentation <https://django-smart-media.readthedocs.io/en/latest/install.html#configuration>`_.

Finally you will have to apply database migrations.


Description editor
******************

The description field from ``AppsBanner`` model use the Django builtin ``Textarea``
widget on default.

However inside a DjangoCMS project it will adopt the editor widget enabled from either
`djangocms-text-ckeditor`_ or `djangocms-text-ckeditor`_ if installed, in case they are
both installed (which is wrong) the first has highest priority.


Settings
********

These are the default settings you can override in your project settings.

.. automodule:: firm_info.defaults
   :members:
