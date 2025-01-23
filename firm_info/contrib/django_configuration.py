from ..defaults import FIRMINFO_APP_NAME


class FirmInfosDefaultSettings:
    """
    Default application settings class to use with a "django-configuration" class.

    Example:

        You just have to inherit from it in your settings class: ::

            from configurations import Configuration
            from firm_info.contrib.django_configuration import FirmInfosDefaultSettings

            class Dev(FirmInfosDefaultSettings, Configuration):
                FIRMINFO_APP_NAME = "Myclient"

        This will override the setting ``FIRMINFO_APP_NAME``
    """  # noqa: E501

    FIRMINFO_APP_NAME = FIRMINFO_APP_NAME
