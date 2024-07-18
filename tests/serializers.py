from firm_info.factories import (
    AppsBannerFactory, FirmContactFactory, SocialSharingFactory
)
from firm_info.models import FirmContact, Link
from firm_info.serializers import (
    _format_address,
    serialize_firm_apps_banner,
    serialize_firm_complete_info,
    serialize_firm_description,
    serialize_firm_info,
    serialize_firm_logos,
    serialize_firm_social,
    serialize_firm_social_sharing,
)

from .constantes import (
    SERIALIZED_SOCIAL_LINKS
)


def test_serialize_firm_info(db):
    firm_contact_obj = FirmContactFactory()
    queryset = FirmContact.objects.all()
    assert queryset.count() == 1
    expected_output = {
        "email": firm_contact_obj.email,
        "phone": firm_contact_obj.phone_number,
        "address": firm_contact_obj.address,
        "city": firm_contact_obj.city,
        "country": firm_contact_obj.country,
        "full_address": _format_address(
            queryset
            .values(
                "phone_number", "email", "address", "postal_code", "city", "country"
            )
            .first()
        ),
        "postal_code": firm_contact_obj.postal_code,
    }
    assert serialize_firm_info(queryset) == expected_output


def test_serialize_firm_social(db, firm_social_links_objs):
    queryset = Link.objects.all()
    expected_output = SERIALIZED_SOCIAL_LINKS
    assert serialize_firm_social(queryset) == expected_output


def test_serialize_firm_description(db):
    firm_contact_obj = FirmContactFactory()
    queryset = FirmContact.objects.all()
    expected_output = {
        "baseline": firm_contact_obj.baseline,
        "short_description": firm_contact_obj.short_description,
    }
    assert serialize_firm_description(queryset) == expected_output


def test_serialize_firm_social_sharing(db):
    SocialSharingFactory()
    obj = SocialSharingFactory._meta.model.objects.first()
    expected_output = {
        "og_image": obj.og_image,
        "og_description": obj.og_description,
        "og_twitter_site": obj.og_twitter_site,
    }
    assert serialize_firm_social_sharing(obj) == expected_output


def test_serialize_firm_apps_banner(db):
    AppsBannerFactory()
    obj = AppsBannerFactory._meta.model.objects.first()
    expected_output = {
        "title": obj.title,
        "description": obj.description,
        "image": obj.image,
    }
    assert serialize_firm_apps_banner(obj) == expected_output


def test_serialize_firm_logos(db):
    FirmContactFactory()
    obj = FirmContactFactory._meta.model.objects.first()
    expected_output = {
        "logo": obj.logo,
        "logo_invert": obj.logo_invert,
        "favicon": obj.favicon,
    }
    assert serialize_firm_logos(obj) == expected_output


def test_serialize_firm_complete_info(db):
    firm_contact_obj = FirmContactFactory()
    queryset = FirmContact.objects.all()
    assert queryset.count() == 1

    expected_output = {
        "address": firm_contact_obj.address,
        "email": firm_contact_obj.email,
        "phone": firm_contact_obj.phone_number,
        "full_address": _format_address(
            queryset.values(
                "phone_number", "email", "address", "postal_code", "city", "country"
            ).first()
        ),
        "baseline": firm_contact_obj.baseline,
        "city": firm_contact_obj.city,
        "country": firm_contact_obj.country,
        "postal_code": firm_contact_obj.postal_code,
        "short_description": firm_contact_obj.short_description,
        "logo": firm_contact_obj.logo,
        "logo_invert": firm_contact_obj.logo_invert,
        "favicon": firm_contact_obj.favicon,
    }
    serialized_data = serialize_firm_complete_info(queryset)
    assert serialized_data == expected_output
