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


@register.simple_tag(name="firm_contact")
def firm_contact(template_path):
    """
    Renders the template which path is provided as param
    using FirmContact only instance serialized contact data.

    - Usage:

    ```html
    {% load firm_info %}

    {% firm_contact "path/to/template.html" %}
    ```

    - Improvement:

    Could use a cached template loader instead of loader.get_template()

    ```python
    from django.core.cache import cache

    template_cache_key = f'firm_contact_template_{template_path}'
    template = cache.get(template_cache_key)
    if template is None:
        cache.set(...)
    contact_cache_key = f'firm_contact_info'
    contact = cache.get(contact_cache_key)
    if contact is None:
        contact = FirmContact.objects.first()
        cache.set(...)
    ```
    """
    qs_firm_info = FirmContact.objects.all()
    if qs_firm_info.exists():
        template = loader.get_template(template_path)
        context = serialize_firm_info(qs_firm_info)
        rendered = template.render(context)
        return rendered
    else:
        return ''


@register.simple_tag(name="firm_social_links")
def firm_social_links(template_path):
    """
    Renders the template which path is provided as param
    using all social network link objects serialized data
    related the only FirmContact instance.

    Usage:
    ```
    html
    {% load firm_info %}

    {% firm_social_links "path/to/template.html" %}
    ```
    """
    links = Link.objects.all()
    if links.exists():
        template = loader.get_template(template_path)
        context = serialize_firm_social(links)
        rendered = template.render(context)
        return rendered
    else:
        return ''


@register.simple_tag(name="firm_description")
def firm_description(template_path):
    """
    Renders the template which path is provided as param
    using FirmContact only instance serialized description data.

    Usage:
    ```
    html
    {% load firm_info %}

    {% firm_description "path/to/template.html" %}
    ```
    """
    qs_firm_info = FirmContact.objects.all()
    if qs_firm_info.exists():
        template = loader.get_template(template_path)
        context = serialize_firm_description(qs_firm_info)
        rendered = template.render(context)
        return rendered
    else:
        return ''


@register.simple_tag(name="firm_logos")
def firm_logos(template_path):
    """
    Renders the template which path is provided as param
    using Firm logos.

    Usage:
    ```
    html
    {% load firm_info %}

    {% firm_logos "path/to/template.html" %}
    ```
    """
    firm_instance = FirmContact.objects.first()
    if firm_instance:
        template = loader.get_template(template_path)
        context = {
            "logo": getattr(firm_instance, "logo", None),
            "logo_invert": getattr(firm_instance, "logo_invert", None),
            "favicon": getattr(firm_instance, "favicon", None),
        }
        rendered = template.render(context)
        return rendered
    else:
        return ''


@register.simple_tag(name="firm_social_shares")
def firm_social_shares(template_path):
    """
    Renders the template which path is provided as param
    using all social network shares link objects serialized data
    related the only SocialSharing instance.

    Usage:
    ```
    html
    {% load firm_info %}

    {% firm_social_shares "path/to/template.html" %}
    ```
    """
    social_shares = SocialSharing.objects.first()

    if social_shares:
        template = loader.get_template(template_path)
        context = serialize_firm_social_sharing(social_shares)
        rendered = template.render(context)

        return rendered
    else:
        return ''


@register.filter("firm_tag_analytic")
def firm_tag_analytic(value=None):
    return Tracking.objects.first().tag_analytic if Tracking.objects.exists() else ""


@register.simple_tag(name="app_banner")
def app_banner(app_type, template_path):
    context = {}
    template = loader.get_template(template_path)

    try:
        app_banner = AppsBanner.objects.get(application_type=app_type)
        context = serialize_firm_apps_banner(app_banner)
    except ObjectDoesNotExist:
        pass

    rendered = template.render(context)

    return rendered
