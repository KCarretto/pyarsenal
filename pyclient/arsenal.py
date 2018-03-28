"""
This module contains shared resources that modules in the library can use.
"""
import requests
from requests.exceptions import ContentDecodingError

from .config import TEAMSERVER_URI
from .exceptions import ServerConnectionError, ServerInternalError

class ArsenalObject(object): # pylint: disable=too-few-public-methods
    """
    This object contains common-purpose functions that other modules will inherit from.
    """
    raw_json = None

    def __init__(self, object_json):
        """
        This constructor takes json and sets the objects attributes accordingly.
        """
        self.raw_json = object_json
        for key, value in object_json.items():
            self.__setattr__(key, value)

    @property
    def json(self, arsenal_object):
        """
        Get a JSON representation of the object.
        """
        pass

    @staticmethod
    def _call(method, **kwargs):
        """
        Helper used to call API functions.
        """
        params = {}

        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        params['method'] = method

        try:
            return requests.post(TEAMSERVER_URI, json=params).json()
        except ContentDecodingError:
            raise ServerInternalError("Teamserver encountered an unexpected error.")
        except Exception as exception:
            raise ServerConnectionError("Could not connect to teamserver. {}".format(exception))
