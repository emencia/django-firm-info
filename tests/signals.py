from os.path import exists

from firm_info.factories import (
    AppsBannerFactory,
    SocialSharingFactory,
    create_image_file,
    FirmContactFactory,
)


def post_delete_FirmContact(db):
    firm_contact = FirmContactFactory()
    files = ["logo", "logo_invert", "favicon"]
    for file in files:
        assert exists(getattr(firm_contact, file).path)
    firm_contact.delete()
    for file in files:
        assert not exists(getattr(firm_contact, file).path)


def post_save_FirmContact(db):
    firm_contact = FirmContactFactory()
    files = ["logo", "logo_invert", "favicon"]

    old_paths = []
    for file in files:
        path = getattr(firm_contact, file).path
        assert exists(path)
        old_paths.append(path)

    firm_contact.logo = create_image_file()
    firm_contact.logo_invert = create_image_file()
    firm_contact.favicon = create_image_file()

    firm_contact.save()

    for path in old_paths:
        assert not exists(path)


def test_post_delete_AppsBanner(db):
    appbanner = AppsBannerFactory()
    assert exists(appbanner.image.path)
    appbanner.delete()
    assert not exists(appbanner.image.path)


def test_post_save_AppsBanner(db):
    appbanner = AppsBannerFactory()
    old_path = appbanner.image.path
    assert exists(old_path)

    appbanner.image = create_image_file()
    appbanner.save()

    assert not exists(old_path)


def test_post_delete_SocialSharing(db):
    socialsharing = SocialSharingFactory()
    assert exists(socialsharing.og_image.path)
    socialsharing.delete()
    assert not exists(socialsharing.og_image.path)


def test_post_save_SocialSharing(db):
    socialsharing = SocialSharingFactory()
    old_path = socialsharing.og_image.path
    assert exists(old_path)

    socialsharing.og_image = create_image_file()
    socialsharing.save()

    assert not exists(old_path)
