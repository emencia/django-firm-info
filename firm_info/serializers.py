from firm_info.exceptions import SerializeFirmError


def _format_address(firm_info: dict) -> str:
    """
    Formats the address using the firm information.

    Args:
        firm_info (dict): The firm information with the following keys:

            - "address": The address of the firm.
            - "postal_code": The postal code of the firm.
            - "city": The city of the firm.
            - "country": The country of the firm.

    Returns:
        str: The formatted address string in the format
          `"{address}, {postal_code} {city} {country}"`.
    """
    return "{}, {} {} {}".format(
        firm_info.get("address", "NOTFOUND"),
        firm_info.get("postal_code", "NOTFOUND"),
        firm_info.get("city", "NOTFOUND"),
        firm_info.get("country", "NOTFOUND"),
    )


def serialize_firm_info(queryset):
    """
    Serializes the firm information from a queryset.

    Args:
        queryset: The queryset containing the firm information.

    Returns:
        dict: the serialized firm information with the following keys:

            - "email": The email address of the firm.
            - "phone": The phone number of the firm.
            - "full_address": The formatted full address of the firm.
            - "address": The address of the firm.
            - "postal_code": The postal code of the firm.
            - "city": The city of the firm.
            - "country": The country of the firm.

    Raises:
        SerializeFirmError: Raised when an error occurs during serialization.
    """

    try:
        firm_info = queryset.values(
            "phone_number", "email", "address", "postal_code", "city", "country"
        ).first()
        return {
            "email": firm_info.get("email"),
            "phone": firm_info.get("phone_number"),
            "full_address": _format_address(firm_info),
            "address": firm_info.get("address"),
            "postal_code": firm_info.get("postal_code"),
            "city": firm_info.get("city"),
            "country": firm_info.get("country"),
        }
    except Exception as err:
        error_msg = "Failed to serialize firm contact."
        raise SerializeFirmError(error_msg) from err


def serialize_firm_social(queryset):
    """
    Serializes the firm social media information from a queryset.

    Args:
        queryset: The queryset containing the firm social media information.

    Returns:
        dict: The serialized firm social media information with the social media names
        as keys and their corresponding URLs as values.

    Raises:
        SerializeFirmError: Raised when an error occurs during serialization.
    """

    try:
        firm_socials = queryset.values("name", "url")
        return {
            social.get("name", "NOTFOUND"): social.get("url", "NOTFOUND")
            for social in firm_socials
        }
    except Exception as err:
        error_msg = "Failed to serialize firm social media information."
        raise SerializeFirmError(error_msg) from err


def serialize_firm_description(queryset):
    """
    Serializes the firm description from a queryset.

    Args:
        queryset: The queryset containing the firm description.

    Returns:
        dict: The serialized firm description with the following keys:

            - "baseline": The baseline of the firm.
            - "short_description": The short description of the firm.

    Raises:
        SerializeFirmError: Raised when an error occurs during serialization.
    """
    try:
        firm_info = queryset.values("baseline", "short_description").first()
        return {
            "baseline": firm_info.get("baseline"),
            "short_description": firm_info.get("short_description"),
        }
    except Exception as err:
        error_msg = "Failed to serialize firm description."
        raise SerializeFirmError(error_msg) from err


def serialize_firm_social_sharing(obj):
    """
    Serialize Firm social networks sharing URLs.

    Args:
        obj (QuerySet): The `SocialSharing` queryset.

    Returns:
        dict: The serialized data with the following keys:

            - og_image (SmartMediaField): The OG image for social media sharing.
            - og_description (TextField): The OG description for social media sharing.
            - og_twitter_site (CharField): The OG Twitter site for social media sharing.

    Raises:
        SerializeFirmError: Raised when an error occurs during serialization.
    """

    try:
        return {
            "og_image": obj.og_image,
            "og_description": obj.og_description,
            "og_twitter_site": obj.og_twitter_site,
        }

    except Exception as err:
        error_msg = "Failed to serialize social sharing information."
        raise SerializeFirmError(error_msg) from err


def serialize_firm_apps_banner(obj):
    """
    Serializes an instance of the AppsBanner model into a dictionary.

    Args:
        obj: The AppsBanner object to be serialized.

    Returns:
        dict: The serialized data with the following keys:

            - "title": The title of the `AppsBanner`.
            - "description": The description of the AppsBanner.
            - "image": The image associated with the AppsBanner.

    Raises:
        SerializeFirmError: Raised when an error occurs during serialization.
"""

    try:
        return {
            "title": obj.title,
            "description": obj.description,
            "image": obj.image,
        }

    except Exception as err:
        error_msg = "Failed to serialize apps banner information."
        raise SerializeFirmError(error_msg) from err


def serialize_firm_logos(obj):
    """
    Serializes logo information from a FirmContact instance.

    Args:
        firm_instance (FirmContact): An instance of FirmContact containing logos.

    Returns:
        dict: A dictionary with logo details suitable for rendering in templates.

    Raises:
        SerializeFirmError: Raised when an error occurs during serialization.
    """
    if obj is None:
        return {}

    try:
        return {
            "logo": getattr(obj, "logo", None),
            "logo_invert": getattr(obj, "logo_invert", None),
            "favicon": getattr(obj, "favicon", None),
        }
    except Exception as err:
        error_msg = "Failed to serialize firm social logos."
        raise SerializeFirmError(error_msg) from err


def serialize_firm_complete_info(queryset):
    """
    Serializes complete firm information from a FirmContact instance.

    Args:
        firm_instance (FirmContact): An instance of FirmContact.

    Returns:
        dict: The serialized complete firm information, including logos and
        descriptions.

    Raises:
        SerializeFirmError: Raised when an error occurs during serialization.
    """
    if not queryset.exists():
        return {}

    try:
        return {
            **serialize_firm_info(queryset),
            **serialize_firm_description(queryset),
            **serialize_firm_logos(queryset.first()),
        }
    except Exception as err:
        error_msg = "Failed to serialize firm social complete information."
        raise SerializeFirmError(error_msg) from err
