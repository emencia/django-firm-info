from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from smart_media.admin import SmartModelAdmin

from .forms import AppsBannerForm
from .models import AppsBanner, FirmContact, Link, SocialSharing, Tracking


class UniqueModelAdmin(admin.ModelAdmin):
    """
    A custom ModelAdmin that restricts the addition of model instances to only one.

    This admin class overrides the default add permission to ensure that only one
    instance of the associated model can exist at any given time.
    If an instance already exists, it prohibits adding new instances.
    """

    def has_add_permission(self, request):
        existing_count = self.model.objects.count()
        if existing_count == 0:
            return super().has_add_permission(request)
        else:
            return False

    def clean(self):
        existing_count = self.model.objects.count()
        if existing_count > 1:
            # raise validation error if there is more than one firm contact
            raise ValidationError(
                _("Only one {} instance is allowed.").format(self.model.__name__)
            )


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


@admin.register(FirmContact)
class ClientContactAdmin(UniqueModelAdmin):
    inlines = [LinkInline]
    formfield_overrides = SmartModelAdmin.formfield_overrides


@admin.register(SocialSharing)
class SocialSharingAdmin(UniqueModelAdmin):
    pass


@admin.register(Tracking)
class TrackingAdmin(UniqueModelAdmin):
    pass


@admin.register(AppsBanner)
class AppsBannerAdmin(admin.ModelAdmin):
    formfield_overrides = SmartModelAdmin.formfield_overrides
    form = AppsBannerForm
