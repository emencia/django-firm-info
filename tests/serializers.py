from firm_info.models import FirmContact, Link
from firm_info.serializers import (
    _format_address,
    serialize_firm_description,
    serialize_firm_info,
    serialize_firm_social,
)

from .constantes import (
    SERIALIZED_SOCIAL_LINKS
)


def test_serialize_firm_info(db, firm_contact_obj):
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


def test_serialize_firm_description(db, firm_contact_obj):
    queryset = FirmContact.objects.all()
    expected_output = {
        "baseline": firm_contact_obj.baseline,
        "short_description": firm_contact_obj.short_description,
    }
    assert serialize_firm_description(queryset) == expected_output
