class SerializeFirmError(Exception):
    """
    Custom exception to handle errors during Firm informations serialization.
    """

    pass


def _format_address(firm_info: dict) -> str:
    return "{}, {} {} {}".format(
        firm_info.get("address"),
        firm_info.get("postal_code"),
        firm_info.get("city"),
        firm_info.get("country"),
    )


def serialize_firm_info(queryset):
    """
    Serialize FirmContact unique instance.


    Args:
        `FirmContact` Queryset

    Raises:
        SerializeFirmError

    Returns:
        (dict): email phone and address of firm as serialized data

        Sample:
        ```
        {
            "email": "email@mail.com",
            "phone": "003369856321",
            "address": "1 avenue Charles de Gaulle, 99999 Paris"
        }
        ```
    """
    try:
        firm_info = queryset.values(
            "phone_number", "email", "address", "postal_code", "city", "country"
        ).first()
        return {
            "email": firm_info.get("email"),
            "phone": firm_info.get("phone_number"),
            "address": _format_address(firm_info),
        }
    except Exception as err:
        raise SerializeFirmError from err


def serialize_firm_social(queryset):
    """
    Serialize Firm social networks urls.

    Args:
        `Link` Queryset

    Raises:
        SerializeFirmError

    Returns:
        (dict): social network name as dict key, url as dict value.

        Sample:
        ```python
        {
            "facebook": "www.site.com",
            "instagram": "www.site2.com"
        }
        ```
    """
    try:
        firm_socials = list(
            queryset.values(
                "name",
                "url",
            )
        )
        return {
            social.get("name", "NOTFOUND"): social.get("url", "NOTFOUND")
            for social in firm_socials
        }
    except Exception as err:
        raise SerializeFirmError from err


def serialize_firm_description(queryset):
    """
    Serialize FirmContact unique instance.


    Args:
        `FirmContact` Queryset

    Raises:
        SerializeFirmError

    Returns:
        (dict): baseline and short_description of firm as serialized data

        Sample:
        ```
        {
            "baseline": "Non eram nescius, Brute, cum, quae summis ingeniis",
            "short_description": "Quamquam, si plane sic verterem Platonem"
        }
        ```
    """
    try:
        firm_info = queryset.values("baseline", "short_description").first()
        return {
            "baseline": firm_info.get("baseline"),
            "short_description": firm_info.get("short_description"),
        }
    except Exception as err:
        raise SerializeFirmError from err


def serialize_firm_social_sharing(obj):
    """
    Serialize Firm social networks sharing urls.

    Args:
        `SocialSharing` Queryset

    Raises:
        SerializeFirmError

    Returns:
        (dict): og_image, og_description and og_twitter_site as serialized data

        Sample:
        ```python
        {
            "og_image": SmartMediaField(),
            "og_description": TextField(),
            "og_twitter_site": CharField(),
        }
        ```
    """

    try:
        return {
            "og_image": obj.og_image,
            "og_description": obj.og_description,
            "og_twitter_site": obj.og_twitter_site,
        }

    except Exception as err:
        raise SerializeFirmError from err


def serialize_firm_apps_banner(obj):
    try:
        return {
            "title": obj.title,
            "description": obj.description,
            "image": obj.image,
        }

    except Exception as err:
        raise SerializeFirmError from err
