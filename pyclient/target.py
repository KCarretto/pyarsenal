"""
This module contains Target API functions.
"""
from .exceptions import parse_error
from .objects import Target

def create_target(
        self,
        name,
        mac_addrs,
        facts):
    """
    This method creates a Target on the teamserver.
    """
    resp = self.call(
        'CreateTarget',
        name=name,
        mac_addrs=mac_addrs,
        facts=facts)

    if resp.get('error', True):
        parse_error(resp)

def get_target(self, name, **kwargs):
    """
    Returns a Target object from the teamserver.
    """
    resp = self._get_target_raw(name, kwargs) # pylint: disable=protected-access

    if resp.get('error', True):
        parse_error(resp)

    return Target(resp['target'])

def _get_target_raw(self, name, params):
    """
    Returns the raw response of the GetTarget API call.
    """
    return self.call(
        'GetTarget',
        name=name,
        include_status=params.get('include_status', True),
        include_facts=params.get('include_facts', False),
        include_sessions=params.get('include_sessions', False),
        include_actions=params.get('include_actions', False),
        include_groups=params.get('include_groups', False),
        include_credentials=params.get('include_credentials', False),
    )

def rename_target(self, name, new_name):
    """
    Renames a Target object on the teamserver.
    """
    resp = self.call(
        'RenameTarget',
        name=name,
        new_name=new_name)
    if resp.get('error', True):
        parse_error(resp)

def set_target_facts(self, name, facts):
    """
    Override Target facts with updated information.
    """
    resp = self.call(
        'GetTarget',
        name=name,
        facts=facts)
    if resp.get('error', True):
        parse_error(resp)

def list_targets(self, **kwargs):
    """
    Returns a list of Target Objects from the teamserver.
    """
    resp = self._list_targets_raw(kwargs) # pylint: disable=protected-access

    if resp.get('error', True):
        parse_error(resp)

    return [Target(target) for name, target in resp['targets'].items()]

def _list_targets_raw(self, params):
    """
    Returns the raw response of the ListTargets API call.
    """
    return self.call(
        'ListTargets',
        include_status=params.get('include_status', True),
        include_facts=params.get('include_facts', False),
        include_sessions=params.get('include_sessions', False),
        include_actions=params.get('include_actions', False),
        include_groups=params.get('include_groups', False),
        include_credentials=params.get('include_credentials', False),
    )
