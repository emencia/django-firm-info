"""
Specific application exceptions.
"""


class MyAppBaseException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class SerializeFirmError(MyAppBaseException):
    """
    Exceptions related to FirmContact serialization errors
    during template tag generation.
    """
    pass
