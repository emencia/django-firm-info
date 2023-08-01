from django.db import models
from django.utils.translation import gettext_lazy as _


class SingletonManager(models.Manager):
    def create(self, **kwargs):
        if self.model.objects.exists():
            error_message = _("Model {model_name} has already one instance")
            raise ValueError(
                error_message.format(model_name=self.model._meta.verbose_name)
            )
        return super().create(**kwargs)
