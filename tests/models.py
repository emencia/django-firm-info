import pytest

from firm_info.factories import (
    FirmContactFactory, SocialSharingFactory, TrackingFactory
)
from firm_info.managers import SINGLETON_ERROR


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
