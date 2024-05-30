import pytest

from html import unescape

from django.template import RequestContext, Template
from django.test import RequestFactory

from firm_info.models import FirmContact, Link
from firm_info.factories import TrackingFactory
from firm_info.templatetags.firm_info import (
    firm_contact,
    firm_description,
    firm_social_links,
    firm_tag_analytic,
)

from .constantes import SERIALIZED_SOCIAL_LINKS


def test_firm_contact_tag(db, firm_contact_obj):
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


def test_firm_description_tag(firm_contact_obj):
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


def test_firm_tag_analytic(db):
    # test on empty db
    assert "" == firm_tag_analytic()
    # add on tag
    tracking = TrackingFactory(tag_analytic="G-XXX-YYY")
    assert tracking.tag_analytic == firm_tag_analytic()
    # add a second tag
    tracking2 = TrackingFactory(tag_analytic="B-XXX-YYY")
    # main tag is still the first one
    assert tracking2.tag_analytic != firm_tag_analytic()
    assert tracking.tag_analytic == firm_tag_analytic()
    # remove the first tag, tracking2 is the new main tag
    tracking.delete()
    assert tracking2.tag_analytic == firm_tag_analytic()
