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
    groups = None
    actions = None

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
    def get_target( #pylint: disable=too-many-arguments
            name, **kwargs):
            # include_status=True,
            # include_facts=False,
            # include_sessions=False,
            # include_actions=False,
            # include_groups=False,
            # include_credentials=False):
        """
        Returns a Target object from the teamserver.
        """
        resp = Target._get_target_raw(name, kwargs)

        if resp.get('error', True):
            parse_error(resp)

        return Target(resp['target'])

    @staticmethod
    def _get_target_raw( #pylint: disable=too-many-arguments
            name,
            params):
        """
        Returns the raw response of the GetTarget API call.
        """
        return ArsenalObject._call(
            'GetTarget',
            name=name,
            include_status=params.get('include_status', True),
            include_facts=params.get('include_facts', False),
            include_sessions=params.get('include_sessions', False),
            include_actions=params.get('include_actions', False),
            include_groups=params.get('include_groups', False),
            include_credentials=params.get('include_credentials', False),
        )

    @staticmethod
    def rename_target(name, new_name):
        """
        Renames a Target object on the teamserver.
        """
        resp = ArsenalObject._call(
            'RenameTarget',
            name=name,
            new_name=new_name)
        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def set_target_facts(name, facts):
        """
        Override Target facts with updated information.
        """
        resp = ArsenalObject._call(
            'GetTarget',
            name=name,
            facts=facts)
        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def list_targets(**kwargs):
        """
        Returns a list of Target Objects from the teamserver.
        """
        resp = Target._list_targets_raw(kwargs)

        if resp.get('error', True):
            parse_error(resp)

        return [Target(target) for name, target in resp['targets'].items()]

    @staticmethod
    def _list_targets_raw(params):
        """
        Returns the raw response of the ListTargets API call.
        """
        return ArsenalObject._call(
            'ListTargets',
            include_status=params.get('include_status', True),
            include_facts=params.get('include_facts', False),
            include_sessions=params.get('include_sessions', False),
            include_actions=params.get('include_actions', False),
            include_groups=params.get('include_groups', False),
            include_credentials=params.get('include_credentials', False),
        )
