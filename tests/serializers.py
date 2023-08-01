from firm_info.models import FirmContact, Link
from firm_info.serializers import (
    serialize_firm_description,
    serialize_firm_info,
    serialize_firm_social,
)


def test_serialize_firm_info(db, firm_contact_obj, serialized_contact):
    queryset = FirmContact.objects.all()
    expected_output = serialized_contact
    assert serialize_firm_info(queryset) == expected_output


def test_serialize_firm_social(db, firm_social_links_objs, serialized_social_links):
    queryset = Link.objects.all()
    expected_output = serialized_social_links
    assert serialize_firm_social(queryset) == expected_output


def test_serialize_firm_description(db, firm_contact_obj, serialized_firm_description):
    queryset = FirmContact.objects.all()
    expected_output = serialized_firm_description
    assert serialize_firm_description(queryset) == expected_output
