from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.translation import gettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from firm_info.managers import SingletonManager
from smart_media.modelfields import SmartMediaField
from smart_media.signals import auto_purge_files_on_change, auto_purge_files_on_delete


class FirmContact(models.Model):
    """
    Represents the contact information for a firm.

    Args:
        models.Model: The base model class provided by Django.

    Attributes:
        phone_number (CharField): The phone number of the firm.
        email (EmailField): The email address of the firm.
        address (CharField): The address of the firm.
        postal_code (CharField): The postal code of the firm.
        city (CharField): The city of the firm.
        country (CharField): The country of the firm.
        baseline (CharField): The baseline of the firm.
        short_description (TextField): The short description of the firm.
        logo (SmartMediaField): The logo of the firm.
        logo_invert (SmartMediaField): The inverted logo of the firm.
        favicon (SmartMediaField): The favicon of the firm.
        objects (SingletonManager): The manager for the FirmContact model.
    """
    phone_number = models.CharField(max_length=20, null=False, blank=True, default="")
    email = models.EmailField(null=False, blank=True, default="")
    address = models.CharField(max_length=255, null=False, blank=True, default="")
    postal_code = models.CharField(max_length=20, null=False, blank=True, default="")
    city = models.CharField(max_length=100, null=False, blank=True, default="")
    country = models.CharField(max_length=100, null=False, blank=True, default="")
    baseline = models.CharField(max_length=255, null=False, blank=True, default="")
    short_description = models.TextField(null=False, blank=True, default="")
    logo = SmartMediaField(
        _("Logo"),
        null=True,
        blank=True,
        upload_to="firm_info/firm_contact/logo/%y/%m",
    )
    logo_invert = SmartMediaField(
        _("Logo invert"),
        null=True,
        blank=True,
        upload_to="firm_info/firm_contact/logo_invert/%y/%m",
    )
    favicon = SmartMediaField(
        _("Favicon"),
        null=True,
        blank=True,
        upload_to="firm_info/firm_contact/favicon/%y/%m",
    )

    objects = SingletonManager()

    class Meta:
        verbose_name = _("Company contact information")
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(_("Client information"))


post_delete.connect(
    auto_purge_files_on_delete(["logo", "logo_invert", "favicon"]),
    dispatch_uid="firm_info_firm_contact_medias_on_delete",
    sender=FirmContact,
    weak=False,
)

pre_save.connect(
    auto_purge_files_on_change(["logo", "logo_invert", "favicon"]),
    dispatch_uid="firm_info_firm_contact_medias_on_change",
    sender=FirmContact,
    weak=False,
)


class Link(models.Model):
    """
    Represents a social network link.

    Attributes:
        SOCIAL_NETWORK_NAMES (tuple): Choices for the name field representing
            various social network names.
        name (CharField): The name of the social network.
        url (URLField): The URL of the social network link.
        client_contact (ForeignKey): The foreign key to the FirmContact model
            representing the client contact.
    """
    SOCIAL_NETWORK_NAMES = (
        ("linkedin", "linkedin"),
        ("facebook", "facebook"),
        ("twitter", "twitter"),
        ("youtube", "youtube"),
        ("instagram", "instagram"),
        ("glassdoor", "glassdoor"),
        ("bitbucket", "bitbucket"),
        ("github", "github"),
        ("gitlab", "gitlab"),
        ("tiktok", "tiktok"),
        ("twitch", "twitch"),
        ("discord", "discord"),
        ("vk", "vk"),
        ("slack", "slack"),
        ("whatsapp", "whatsapp"),
        ("weechat", "weechat"),
    )

    name = models.CharField(max_length=255, choices=SOCIAL_NETWORK_NAMES)
    url = models.URLField(max_length=255)
    client_contact = models.ForeignKey(FirmContact, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.url}"

    class Meta:
        verbose_name = _("Social network link")
        verbose_name_plural = _("Social networks links")


class SocialSharing(models.Model):
    """
    Represents social media sharing information.

    Attributes:
        og_image (SmartMediaField): The OG image for social media sharing.
        og_description (TextField): The OG description for social media sharing.
        og_twitter_site (CharField): The OG Twitter site for social media sharing.
    """

    og_image = SmartMediaField(
        _("OG Image"),
        null=True,
        blank=True,
        upload_to="firm/social_sharing/%y/%m",
    )
    og_description = models.TextField(
        max_length=180,
        null=False,
        blank=True,
        default="",
        verbose_name=_("OG Description"),
    )
    og_twitter_site = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        default="",
        verbose_name=_("OG Twitter Site"),
    )

    class Meta:
        verbose_name = _("Social media share")
        verbose_name_plural = _("Social media shares")


post_delete.connect(
    auto_purge_files_on_delete(["og_image"]),
    dispatch_uid="socialsharing_medias_on_delete",
    sender=SocialSharing,
    weak=False,
)

pre_save.connect(
    auto_purge_files_on_change(["og_image"]),
    dispatch_uid="socialsharing_medias_on_change",
    sender=SocialSharing,
    weak=False,
)


class Tracking(models.Model):
    """
    Represents tracking information.

    Attributes:
        tag_analytic (CharField): The tag analytic for tracking.
    """

    tag_analytic = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        default="",
        verbose_name=_("Tag Analytic"),
    )

    class Meta:
        verbose_name = _("Tracking")
        verbose_name_plural = _("Tracks")


class AppsBanner(models.Model):
    """
    Represents an app banner in the Django firm_info models.

    Args:
        models.Model: The base model class provided by Django.

    Attributes:
        APPS_CHOICES (list): A list of tuples representing the available choices for
            the application type.
        application_type (models.CharField): The type of the application.
        image (SmartMediaField): The image associated with the app banner.
        title (models.CharField): The title of the app banner.
        description (HTMLField): The description of the app banner.
    """

    APPS_CHOICES = [
        ("application_sent", _("Application sent")),
        ("free_apply", _("Free apply")),
        ("job_offers", _("Job offers")),
        ("news", _("News")),
        ("trombinoscope", _("Trombinoscope")),
    ]

    application_type = models.CharField(
        max_length=16, choices=APPS_CHOICES, unique=True
    )
    image = SmartMediaField(
        _("Image"),
        null=True,
        blank=True,
        upload_to="firm/apps_banner/%y/%m",
    )
    title = models.CharField(_("Title"), max_length=150, blank=True, null=True)
    description = HTMLField(verbose_name=_("Description"), blank=True, null=True)

    def __str__(self):
        return self.get_application_type_display()

    class Meta:
        verbose_name = _("App banner")
        verbose_name_plural = _("App banners")


post_delete.connect(
    auto_purge_files_on_delete(["image"]),
    dispatch_uid="apps_banner_medias_on_delete",
    sender=AppsBanner,
    weak=False,
)

pre_save.connect(
    auto_purge_files_on_change(["image"]),
    dispatch_uid="apps_banner_medias_on_change",
    sender=AppsBanner,
    weak=False,
)
