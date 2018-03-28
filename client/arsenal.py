"""
This module contains shared resources that modules in the library can use.
"""
import requests

from client.config import TEAMSERVER_URI

class ArsenalObject(object): # pylint: disable=too-few-public-methods
    """
    This object contains common-purpose functions that other modules will inherit from.
    """
    def __init__(self, object_json):
        """
        This constructor takes json and sets the objects attributes accordingly.
        """
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

        return requests.post(TEAMSERVER_URI, json=params).json()
