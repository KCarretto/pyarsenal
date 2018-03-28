"""
This module contains exceptions raised by the pyclient library.
"""
from functools import wraps

class ServerConnectionError(Exception):
    """
    Raised when the client cannot connect to the teamserver.
    """
    pass

class ServerInternalError(Exception):
    """
    Raised when the teamserver encounters an unhandled error, and does not return proper json.
    """
    pass

class APIException(Exception):
    """
    Raised when the teamserver API returns an error.
    """
    pass

class SessionNotFound(APIException):
    """
    Raised when a Session was queried, and does not exist.
    """
    pass

class TargetNotFound(APIException):
    """
    Raised when a Target was not found.
    """
    pass

def handle_exceptions(func):
    """
    This function can be used as a decorator to wrap functions.
    Wrapped functions will be surrounded in a try / except block that
    includes necessary error handling, including logging and
    returning error responses.
    """

    @wraps(func)
    def wrapper(*args, **kwargs): #pylint: disable=too-many-return-statements
        """
        This uses the func tools library to wrap a function.
        """
        try:
            retval = func(*args, **kwargs)
            return retval

        except ServerConnectionError:
            print("Error: Could not connect to teamserver.")

        except ServerInternalError:
            print("Error: Teamserver encountered unexpected error")

    return wrapper
