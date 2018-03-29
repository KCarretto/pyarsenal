"""
This module contains Log API functions.
"""
from .arsenal import ArsenalObject
from .exceptions import parse_error

class Target(ArsenalObject):
    """
    This object represents a Target from the teamserver.
    """
    name = None
    status = None
    lastseen = None
    mac_addrs = None
    facts = None
    sessions = None
    credentials = None

    @staticmethod
    def create_target(
            name,
            mac_addrs,
            facts):
        """
        This method creates a Target on the teamserver.
        """
        resp = ArsenalObject._call(
            'CreateTarget',
            name=name,
            mac_addrs=mac_addrs,
            facts=facts)

        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def get_target(name):
        """
        Returns a Target object from the teamserver.
        """
        resp = Target._get_target_raw(name)
        if resp.get('error', True):
            parse_error(resp)

        return Target(resp['target'])

    @staticmethod
    def _get_target_raw(name):
        """
        Returns the raw response of the GetTarget API call.
        """
        return ArsenalObject._call(
            'GetTarget',
            name=name)

    @staticmethod
    def list_targets():
        """
        Returns a list of Target Objects from the teamserver.
        """
        resp = Target._list_targets_raw()

        if resp.get('error', True):
            parse_error(resp)

        return [Target(target) for name, target in resp['targets'].items()]

    @staticmethod
    def _list_targets_raw():
        """
        Returns the raw response of the ListTargets API call.
        """
        return ArsenalObject._call(
            'ListTargets'
        )

    @staticmethod
    def list_target_groups(name):
        """
        Returns a list of groups that the Target is in.
        """
        resp = Target._list_target_groups_raw(name)

        if resp.get('error', True):
            parse_error(resp)

        return resp.get('groups', [])

    @staticmethod
    def _list_target_groups_raw(name):
        """
        Returns a list of groups that the Target is in.
        """
        return ArsenalObject._call(
            'ListGroups',
            name=name
        )
