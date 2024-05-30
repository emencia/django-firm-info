import pytest
from firm_info.factories import FirmContactFactory
from firm_info.models import Link
from .constantes import RAW_SOCIAL_LINKS


@pytest.fixture()
def firm_contact_obj(db):
    return FirmContactFactory()


@pytest.fixture()
def firm_social_links_objs(db, firm_contact_obj):
    links = [
        Link(client_contact=firm_contact_obj, **data) for data in RAW_SOCIAL_LINKS
    ]
    Link.objects.bulk_create(links)
    return Link.objects.filter(client_contact=firm_contact_obj)
