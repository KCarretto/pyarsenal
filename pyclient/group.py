"""
This module contains Group API functions.
"""
from .exceptions import parse_error
from .objects import Group

def create_group(self, name):
    """
    This method creates a Group on the teamserver.
    """
    resp = self.call(
        'CreateGroup',
        name=name,)

    if resp.get('error', True):
        parse_error(resp)

def get_group(self, name):
    """
    This method fetches a Group object from the teamserver.
    """

    resp = self._get_group_raw(name) # pylint: disable=protected-access

    if resp.get('error', True):
        parse_error(resp)

    return Group(resp.get('group'))

def _get_group_raw(self, name):
    """
    Returns the raw response of the GetGroup API call.
    """
    return self.call(
        'GetGroup',
        name=name,
    )

def add_group_member(self, group_name, target_name):
    """
    This method whitelists a Target as a member of a Group.
    """
    resp = self.call(
        'AddGroupMember',
        group_name=group_name,
        target_name=target_name)

    if resp.get('error', True):
        parse_error(resp)

def remove_group_member(self, group_name, target_name):
    """
    This method removes a Target from the whitelist of a Group.
    """
    resp = self.call(
        'RemoveGroupMember',
        group_name=group_name,
        target_name=target_name)

    if resp.get('error', True):
        parse_error(resp)

def blacklist_group_member(self, group_name, target_name):
    """
    This method removes a Target from the whitelist of a Group.
    It also prevents any automember rules from including the Target.
    """
    resp = self.call(
        'BlacklistGroupMember',
        group_name=group_name,
        target_name=target_name)

    if resp.get('error', True):
        parse_error(resp)

def delete_group(self, name):
    """
    This method deletes a Group from the teamserver.
    """
    resp = self.call(
        'DeleteGroup',
        name=name,)

    if resp.get('error', True):
        parse_error(resp)

def list_groups(self):
    """
    This method returns a list of Group objects on the teamserver.
    """
    resp = self._list_groups_raw() # pylint: disable=protected-access

    if resp.get('error', True):
        parse_error(resp)

    return [Group(group) for name, group in resp.get('groups', {}).items()]

def _list_groups_raw(self):
    """
    Returns the raw response of the ListGroups API call.
    """
    return self.call(
        'ListActions'
    )
