import pytest
from firm_info.models import FirmContact, Link


@pytest.fixture
def raw_contact():
    return {
        "phone_number": "1234567890",
        "email": "contact@example.com",
        "address": "1234 Main St",
        "postal_code": "12345",
        "city": "Anytown",
        "country": "USA",
        "baseline": "Non eram nescius, Brute, cum, quae summis ingeniis",
        "short_description": "Quamquam, si plane sic verterem Platonem"
    }


@pytest.fixture
def raw_social_links():
    return [
        {"name": "facebook", "url": "http://facebook.com/example"},
        {"name": "twitter", "url": "http://twitter.com/example"},
    ]


@pytest.fixture
def serialized_contact():
    return {
        "email": "contact@example.com",
        "phone": "1234567890",
        "address": "1234 Main St, 12345 Anytown USA"
    }


@pytest.fixture
def serialized_social_links():
    return {
        "facebook": "http://facebook.com/example",
        "twitter": "http://twitter.com/example",
    }


@pytest.fixture
def serialized_firm_description():
    return {
        "baseline": "Non eram nescius, Brute, cum, quae summis ingeniis",
        "short_description": "Quamquam, si plane sic verterem Platonem"
    }


@pytest.fixture
def firm_contact_obj(raw_contact):
    return FirmContact.objects.create(**raw_contact)


@pytest.fixture
def firm_social_links_objs(firm_contact_obj, raw_social_links):
    links = [
        Link(client_contact=firm_contact_obj, **data) for data in raw_social_links
    ]
    Link.objects.bulk_create(links)
    return Link.objects.filter(client_contact=firm_contact_obj)
