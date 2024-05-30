import contextlib
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, loader
from firm_info.models import AppsBanner, FirmContact, Link, SocialSharing, Tracking
from firm_info.serializers import (
    serialize_firm_apps_banner,
    serialize_firm_description,
    serialize_firm_info,
    serialize_firm_social,
    serialize_firm_social_sharing,
)

register = Library()


@register.simple_tag(takes_context=True, name="firm_contact")
def firm_contact(context, template_path):
    """
    Renders the template which path is provided as param
    using FirmContact only instance serialized contact data.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The rendered HTML output of the firm contact informations.

    Usage:

    .. code-block:: html

        {% load firm_info %}
        {% firm_contact "path/to/template.html" %}

    """
    qs_firm_info = FirmContact.objects.all()
    if qs_firm_info.exists():
        template = loader.get_template(template_path)
        specific_context = serialize_firm_info(qs_firm_info)
        combined_context = {**context.flatten(), **specific_context}
        rendered = template.render(combined_context)
        return rendered
    else:
        return ''


@register.simple_tag(takes_context=True, name="firm_social_links")
def firm_social_links(context, template_path):
    """
    Renders the template which path is provided as param
    using all social network link objects serialized data
    related the only FirmContact instance.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The rendered HTML output of the firm social networks links.

    Usage:

    .. code-block:: html

        {% load firm_info %}
        {% firm_social_links "path/to/template.html" %}

    """
    links = Link.objects.all()
    if links.exists():
        template = loader.get_template(template_path)
        specific_context = serialize_firm_social(links)
        combined_context = {**context.flatten(), **specific_context}
        rendered = template.render(combined_context)
        return rendered
    else:
        return ''


@register.simple_tag(takes_context=True, name="firm_description")
def firm_description(context, template_path):
    """
    Renders the template which path is provided as param
    using FirmContact only instance serialized description data.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The rendered HTML output of the firm description.

    Usage:

    .. code-block:: html

        {% load firm_info %}
        {% firm_description "path/to/template.html" %}

    """
    qs_firm_info = FirmContact.objects.all()
    if qs_firm_info.exists():
        template = loader.get_template(template_path)
        specific_context = serialize_firm_description(qs_firm_info)
        combined_context = {**context.flatten(), **specific_context}
        rendered = template.render(combined_context)
        return rendered
    else:
        return ''


@register.simple_tag(takes_context=True, name="firm_logos")
def firm_logos(context, template_path):
    """
    Renders the firm logos using the specified template.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The rendered HTML output of the firm logos.

    Usage:

    .. code-block:: html

        {% load firm_info %}
        {% firm_logos "path/to/template.html" %}

    """
    firm_instance = FirmContact.objects.first()
    if firm_instance:
        template = loader.get_template(template_path)
        specific_context = {
            "logo": getattr(firm_instance, "logo", None),
            "logo_invert": getattr(firm_instance, "logo_invert", None),
            "favicon": getattr(firm_instance, "favicon", None),
        }
        combined_context = {**context.flatten(), **specific_context}
        rendered = template.render(combined_context)
        return rendered
    else:
        return ''


@register.simple_tag(takes_context=True, name="firm_social_shares")
def firm_social_shares(context, template_path):
    """
    Renders the template which path is provided as param
    using all social network shares link objects serialized data
    related the only SocialSharing instance.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The rendered HTML output of the firm social media shares.

    Usage:

    .. code-block:: html

        {% load firm_info %}
        {% firm_social_shares "path/to/template.html" %}

    """
    social_shares = SocialSharing.objects.first()

    if social_shares:
        template = loader.get_template(template_path)
        specific_context = serialize_firm_social_sharing(social_shares)
        combined_context = {**context.flatten(), **specific_context}
        rendered = template.render(combined_context)

        return rendered
    else:
        return ''


@register.filter("firm_tag_analytic")
def firm_tag_analytic(value=None):
    """
    Filters the firm tag analytic value.

    Args:
        value: The input value (not used).

    Returns:
        str: The tag analytic value from the first Tracking object if it exists,
        otherwise an empty string.

    Usage:

    .. code-block:: html

        {% load firm_info %}
        {% firm_tag_analytic "path/to/template.html" %}

    """
    return Tracking.objects.first().tag_analytic if Tracking.objects.exists() else ""


@register.simple_tag(takes_context=True, name="app_banner")
def app_banner(context, app_type, template_path):
    """
    Renders the app banner using the specified template and application type.

    Args:
        app_type (str): The application type.
        template_path (str): The path to the template file.

    Returns:
        str: The rendered HTML output of the app banner.

    Usage:

    .. code-block:: html

        {% load firm_info %}
        {% app_banner "path/to/template.html" %}

    """
    context = {}
    template = loader.get_template(template_path)

    with contextlib.suppress(ObjectDoesNotExist):
        app_banner = AppsBanner.objects.get(application_type=app_type)
        specific_context = serialize_firm_apps_banner(app_banner)
        combined_context = {**context.flatten(), **specific_context}
    rendered = template.render(combined_context)

    return rendered
