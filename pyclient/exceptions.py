"""
This module contains exceptions raised by the pyclient library.
"""

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
