from django.conf import settings
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FirmInfoAppConfig(AppConfig):
    name = "firm_info"
    verbose_name = _(settings.FIRMINFO_APP_NAME)
    verbose_name_plural = _(settings.FIRMINFO_APP_NAME)
