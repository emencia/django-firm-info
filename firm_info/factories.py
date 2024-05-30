import io

from PIL import Image as PILimage

from django.core.files import File

import factory
from firm_info.models import Tracking

from .models import AppsBanner, FirmContact


def create_image_file(filename=None, size=(100, 100), color="blue",
                      format_name="PNG"):
    """
    Return a File object with a dummy generated image on the fly by PIL or
    possibly a SVG file.

    With default argument values the generated image will be a simple blue
    square in PNG.

    Keyword Arguments:
        filename (string): Filename for created file, default to ``color``
            value joined to extension with ``format`` value in lowercase (or
            ``jpg`` if format is ``JPEG``).
            Note than final filename may be different if all tests use the same
            one since Django will append a hash for uniqueness.
        format_name (string): Format name as available from PIL: ``JPEG``,
            ``PNG`` or ``GIF``. ``SVG`` format is also possible to create a
            dummy SVG file.
        size (tuple): A tuple of two integers respectively for width and height.
        color (string): Color value to fill image, this should be a valid value
            for ``PIL.ImageColor``:
            https://pillow.readthedocs.io/en/stable/reference/ImageColor.html
            or a valid HTML color name for SVG format.

    Returns:
        django.core.files.File: File object.
    """
    ext = format_name.lower()
    # Enforce correct file extension depending format
    if ext == "jpeg":
        ext = "jpg"

    filename = filename or "{}.{}".format(color, ext)

    # Manage correct mode depending format
    mode = "RGB"
    if format_name == "PNG":
        mode = "RGBA"

    # Create a SVG file
    if format_name == "SVG":
        width, height = size
        html = (
            """<svg xmlns="http://www.w3.org/2000/svg" """
            """viewBox="0 0 {width} {height}">"""
            """<path fill="{color}" d="M0 0h{width}v{height}H0z"/>"""
            """</svg>"""
        ).format(
            width=str(width),
            height=str(height),
            color=color,
        )
        thumb_io = io.StringIO(html)
    # Create an image file for every other formats
    else:
        thumb = PILimage.new(mode, size, color)
        thumb_io = io.BytesIO()
        thumb.save(thumb_io, format=format_name)

    return File(thumb_io, name=filename)


class TrackingFactory(factory.django.DjangoModelFactory):
    """
    Create random tag analytic text
    """

    tag_analytic = factory.Faker("text", max_nb_chars=100)

    class Meta:
        model = Tracking


class AppsBannerFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a AppsBanner.
    """

    title = factory.Faker("text", max_nb_chars=150)
    description = factory.Faker("text", max_nb_chars=150)

    class Meta:
        model = AppsBanner

    @factory.lazy_attribute
    def image(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()


class FirmContactFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a FirmContact.
    """

    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    address = factory.Faker("address")
    postal_code = factory.Faker("postcode")
    city = factory.Faker("city")
    country = factory.Faker("country")
    baseline = factory.Faker("text", max_nb_chars=255)
    short_description = factory.Faker("text")

    class Meta:
        model = FirmContact

    @factory.lazy_attribute
    def logo(self):
        return create_image_file()

    @factory.lazy_attribute
    def logo_invert(self):
        return create_image_file()

    @factory.lazy_attribute
    def favicon(self):
        return create_image_file()
