import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from firm_info.models import FirmContact
from tests.utils import get_admin_add_url

from .constantes import RAW_CONTACT


User = get_user_model()


@pytest.fixture
def admin_user():
    # Create an admin user for testing
    admin_user = User.objects.create_superuser("admin", "admin@test.com", "password")
    return admin_user


@pytest.fixture
def admin_client(client, admin_user):
    # Log in the admin user to the client
    client.force_login(admin_user)
    return client


def test_firm_contact_create(db, admin_client):
    # Check that admin client can access the admin interface
    url = reverse("admin:index")
    response = admin_client.get(url)
    assert response.status_code == 200

    # Check that admin can create one FirmContact instance
    url = get_admin_add_url(FirmContact)
    response = admin_client.get(url)
    assert response.status_code == 200

    # needed for post in admin chg
    RAW_CONTACT.update({
        "link_set-TOTAL_FORMS": 1,
        "link_set-INITIAL_FORMS": 0
    })
    response = admin_client.post(url, RAW_CONTACT)
    assert response.status_code == 302

    # Check that the FirmContact instance was created
    qs_firm_contact_values = FirmContact.objects.values(
        "phone_number",
        "email",
        "address",
        "postal_code",
        "city",
        "country",
        "baseline",
        "short_description"
        )
    assert qs_firm_contact_values is not None
    assert all((
        item in RAW_CONTACT.items()
        for item in qs_firm_contact_values[0].items()
    ))

    # Check that the admin can't create another instance
    response = admin_client.post(url, RAW_CONTACT)
    assert response.status_code == 403
    assert FirmContact.objects.filter().count() == 1
