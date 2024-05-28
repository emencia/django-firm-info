from django.db import models
from django.utils.translation import gettext_lazy as _


class SingletonManager(models.Manager):
    """
    A manager to ensure that only one instance of the model exists.

    This manager overrides the `create` method to enforce a singleton pattern
    on the associated model. If an instance of the model already exists,
    attempting to create another instance will raise a `ValueError`.

    Methods:
        create(**kwargs): Creates a new instance of the model if none exists.
            Raises `ValueError` if an instance already exists.
    """
    def create(self, **kwargs):
        if self.model.objects.exists():
            error_message = _("Model {model_name} has already one instance")
            raise ValueError(
                error_message.format(model_name=self.model._meta.verbose_name)
            )
        return super().create(**kwargs)
