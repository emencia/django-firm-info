import pytest
from django.template import Context, Template
from firm_info.models import FirmContact, Link
from firm_info.factories import TrackingFactory
from firm_info.templatetags.firm_info import (
    firm_contact,
    firm_description,
    firm_social_links,
    firm_tag_analytic,
)


def test_firm_contact_tag(db, firm_contact_obj, serialized_contact):
    template_path = "tests/templatetags/firm_info/test_firm_contact.html"
    context = Context()
    context["firm"] = firm_contact_obj
    output = firm_contact(template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        f"<p>Email: {serialized_contact['email']}</p>",
        f"<p>Phone: {serialized_contact['phone']}</p>",
        f"<p>Address: {serialized_contact['address']}</p>"
    ])
    assert rendered == expected_output


def test_firm_social_links_tag(db, firm_social_links_objs, serialized_social_links):
    template_path = "tests/templatetags/firm_info/test_links.html"
    context = Context()
    context["links"] = firm_social_links_objs
    output = firm_social_links(template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        f"<a href=\"{serialized_social_links['facebook']}\">facebook</a><br>",
        f"<a href=\"{serialized_social_links['twitter']}\">twitter</a><br>"
    ])
    assert rendered == expected_output


def test_firm_description_tag(db, firm_contact_obj, serialized_firm_description):
    template_path = "tests/templatetags/firm_info/test_firm_description.html"
    context = Context()
    context["description"] = firm_contact_obj
    output = firm_description(template_path)
    template = Template(output)
    rendered = template.render(context)
    expected_output = "\n".join([
        f"<p>Baseline: {serialized_firm_description['baseline']}</p>",
        f"<p>Short_description: {serialized_firm_description['short_description']}</p>",
    ])
    assert rendered == expected_output


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
    context = Context()
    context["firm"] = Model.objects.none()
    output = firm_contact(template_path)
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
