from ..defaults import (
    CLIENT_NAME,
)


class FirmInfosDefaultSettings:
    """
    Default application settings class to use with a "django-configuration" class.

    Example:

        You just have to inherit from it in your settings class: ::

            from configurations import Configuration
            from firm_info.contrib.django_configuration import FirmInfosDefaultSettings

            class Dev(FirmInfosDefaultSettings, Configuration):
                CLIENT_NAME = "Myclient"

        This will override the setting ``CLIENT_NAME``
    """  # noqa: E501

    CLIENT_NAME = CLIENT_NAME
