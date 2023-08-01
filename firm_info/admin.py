from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from smart_media.admin import SmartModelAdmin

from .models import AppsBanner, FirmContact, Link, SocialSharing, Tracking


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


@admin.register(FirmContact)
class ClientContactAdmin(admin.ModelAdmin):
    inlines = [LinkInline]
    formfield_overrides = SmartModelAdmin.formfield_overrides

    def has_add_permission(self, request):
        existing_count = FirmContact.objects.count()
        if existing_count == 0:
            return super().has_add_permission(request)
        else:
            return False

    def clean(self):
        existing_count = FirmContact.objects.count()
        if existing_count > 1:
            # raise validation error if there is more than one firm contact
            raise ValidationError(_("Only one FirmContact instance allowed."))


@admin.register(SocialSharing)
class SocialSharingAdmin(admin.ModelAdmin):
    pass


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    pass


@admin.register(AppsBanner)
class AppsBannerAdmin(admin.ModelAdmin):
    formfield_overrides = SmartModelAdmin.formfield_overrides
