import pytest

from html import unescape

from django.template import RequestContext, Template
from django.test import RequestFactory

from firm_info.factories import (
    AppsBannerFactory,
    FirmContactFactory,
    SocialSharingFactory
)
from firm_info.models import FirmContact, Link
from firm_info.serializers import _format_address
from firm_info.templatetags.firm_info import (
    app_banner,
    firm_complete_info,
    firm_contact,
    firm_description,
    firm_logos,
    firm_social_links,
    firm_social_shares,
)

from .constantes import SERIALIZED_SOCIAL_LINKS


def test_firm_contact_tag(db):
    firm_contact_obj = FirmContactFactory()
    template_path = "tests/templatetags/firm_info/test_firm_contact.html"

    request = RequestFactory().get('/')
    context = RequestContext(request)

    context["firm"] = firm_contact_obj
    output = firm_contact(context, template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        "<p>Email: {}</p>".format(firm_contact_obj.email),
        "<p>Phone: {}</p>".format(firm_contact_obj.phone_number),
        "<p>Full address: {}, {} {} {}</p>".format(
            firm_contact_obj.address,
            firm_contact_obj.postal_code,
            firm_contact_obj.city,
            firm_contact_obj.country,
        ),
        "<p>Address: {}</p>".format(firm_contact_obj.address),
        "<p>city: {}</p>".format(firm_contact_obj.city),
        "<p>postal code: {}</p>".format(firm_contact_obj.postal_code),
        "<p>country: {}</p>".format(firm_contact_obj.country)
    ])
    assert unescape(rendered) == expected_output


def test_firm_social_links_tag(db, firm_social_links_objs):
    template_path = "tests/templatetags/firm_info/test_links.html"

    request = RequestFactory().get('/')
    context = RequestContext(request)

    context["links"] = firm_social_links_objs
    output = firm_social_links(context, template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        f"<a href=\"{SERIALIZED_SOCIAL_LINKS['facebook']}\">facebook</a><br>",
        f"<a href=\"{SERIALIZED_SOCIAL_LINKS['twitter']}\">twitter</a><br>"
    ])
    assert rendered == expected_output


def test_firm_description_tag(db):
    firm_contact_obj = FirmContactFactory()
    template_path = "tests/templatetags/firm_info/test_firm_description.html"

    factory = RequestFactory()
    request = factory.get('/')
    context = RequestContext(request)

    context["description"] = firm_contact_obj
    output = firm_description(context, template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        f"<p>Baseline: {firm_contact_obj.baseline}</p>",
        f"<p>Short_description: {firm_contact_obj.short_description}</p>",
    ])
    assert unescape(rendered) == expected_output


def test_firm_logos_tag(db):
    firm_contact_obj = FirmContactFactory()
    template_path = "tests/templatetags/firm_info/test_firm_logos.html"

    request = RequestFactory().get('/')
    context = RequestContext(request)

    context["firm"] = firm_contact_obj
    output = firm_logos(context, template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        f"<img src=\"{firm_contact_obj.logo.url}\" alt=\"Logo\">",
        f"<img src=\"{firm_contact_obj.logo_invert.url}\" alt=\"Inverted Logo\">",
        f"<link rel=\"shortcut icon\" href=\"{firm_contact_obj.favicon.url}\">"
    ])
    assert unescape(rendered) == expected_output


@pytest.mark.parametrize(
    "app_type",
    [
        AppsBannerFactory._meta.model.APPS_CHOICES[0][0],
        AppsBannerFactory._meta.model.APPS_CHOICES[1][0]
    ]
)
def test_app_banner(db, app_type):
    template_path = "tests/templatetags/firm_info/test_app_banner.html"

    request = RequestFactory().get('/')
    context = RequestContext(request)

    instance = AppsBannerFactory(application_type=app_type)
    context["app_banner"] = instance
    output = app_banner(context, app_type, template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        "<div id=\"app-banner\">",
        f"<img src=\"{instance.image.url}\" alt=\"{instance.title}\">",
        f"<h1>{instance.title}</h1>",
        f"<p>{instance.description}</p>",
        "</div>"
    ])

    assert unescape(rendered).strip() == expected_output.strip()
    assert unescape(rendered).strip() == expected_output.strip()


def test_firm_social_shares_tag(db):
    template_path = "tests/templatetags/firm_info/test_firm_social_shares.html"

    request = RequestFactory().get('/')
    context = RequestContext(request)

    # Assuming there is at least one SocialSharing instance.
    social_sharing = SocialSharingFactory()

    if social_sharing:
        context["social_sharing"] = social_sharing
        output = firm_social_shares(context, template_path)
        template = Template(output)
        rendered = template.render(context)
        expected_output = "\n".join([
            "<div>",
            f"<img src=\"{social_sharing.og_image.url}\" alt=\"Social Sharing Image\">",
            f"<p>Description: {social_sharing.og_description}</p>",
            f"<p>Twitter Site: {social_sharing.og_twitter_site}</p>",
            "</div>"
        ])
        assert unescape(rendered) == expected_output


@pytest.mark.parametrize(
    "template_path,Model",
    [
        ("tests/templatetags/firm_info/test_firm_contact.html", FirmContact),
        ("tests/templatetags/firm_info/test_links.html", Link),
        ("tests/templatetags/firm_info/test_firm_description.html", FirmContact)
    ]
)
def test_not_rendered_without_objs(db, template_path, Model):
    template_path = template_path

    request = RequestFactory().get('/')
    context = RequestContext(request)

    context["firm"] = Model.objects.none()
    output = firm_contact(context, template_path)
    template = Template(output)
    rendered = template.render(context)
    assert rendered == ""


def test_firm_complete_info_tag(db):
    firm_contact_obj = FirmContactFactory()
    template_path = "tests/templatetags/firm_info/test_firm_complete_info.html"

    request = RequestFactory().get('/')
    context = RequestContext(request)

    context["firm"] = firm_contact_obj
    output = firm_complete_info(context, template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        "<p>Email: {}</p>".format(firm_contact_obj.email),
        "<p>Phone: {}</p>".format(firm_contact_obj.phone_number),
        "<p>Full address: {}, {} {} {}</p>".format(
            firm_contact_obj.address,
            firm_contact_obj.postal_code,
            firm_contact_obj.city,
            firm_contact_obj.country,
        ),
        "<p>Baseline: {}</p>".format(firm_contact_obj.baseline),
        "<p>Description: {}</p>".format(firm_contact_obj.short_description),
        "<img src=\"{}\" alt=\"Logo\">".format(firm_contact_obj.logo.url),
        "<img src=\"{}\" alt=\"Inverted Logo\">".format(firm_contact_obj.logo_invert.url),
        "<link rel=\"shortcut icon\" href=\"{}\">".format(firm_contact_obj.favicon.url)
    ])
    assert unescape(rendered) == expected_output
