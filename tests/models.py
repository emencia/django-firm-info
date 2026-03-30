import pytest
from decimal import Decimal

from firm_info.factories import (
    FirmContactFactory, SocialSharingFactory, TrackingFactory
)
from firm_info.managers import SINGLETON_ERROR


def test_firm_contact_geo_coordinates_fields_exist(db):
    """FirmContact must have optional latitude and longitude fields."""
    firm = FirmContactFactory(latitude=Decimal("48.884500"), longitude=Decimal("2.269400"))
    firm.refresh_from_db()
    assert firm.latitude == Decimal("48.884500")
    assert firm.longitude == Decimal("2.269400")


def test_firm_contact_geo_coordinates_default_to_none(db):
    """latitude and longitude must be nullable/blank."""
    firm = FirmContactFactory()
    firm.refresh_from_db()
    assert firm.latitude is None
    assert firm.longitude is None


def test_singleton_firm_contact(db):
    FirmContactFactory()
    with pytest.raises(
        ValueError,
        match=SINGLETON_ERROR.format(
            model_name=FirmContactFactory._meta.model._meta.verbose_name
        )
    ):
        FirmContactFactory()


def test_singleton_social_sharing(db):
    SocialSharingFactory()
    with pytest.raises(
        ValueError,
        match=SINGLETON_ERROR.format(
            model_name=SocialSharingFactory._meta.model._meta.verbose_name
        )
    ):
        SocialSharingFactory()


def test_singleton_tracking(db):
    TrackingFactory()
    with pytest.raises(
        ValueError,
        match=SINGLETON_ERROR.format(
            model_name=TrackingFactory._meta.model._meta.verbose_name
        )
    ):
        TrackingFactory()
