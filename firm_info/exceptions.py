"""
Specific application exceptions.
"""


class FirmInfoException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class SerializeFirmError(FirmInfoException):
    """Exception raised when serializing firm data encounters an error."""
    pass
