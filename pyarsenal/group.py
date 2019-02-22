"""
This module contains Group API functions.
"""
from pyarsenal.objects import Group

def create_group(self, name):
    """
    This method creates a Group on the teamserver.
    """
    self.call(
        'CreateGroup',
        name=name,
    )
    return True

def get_group(self, name):
    """
    This method fetches a Group object from the teamserver.
    """

    resp = self._get_group_raw(name) # pylint: disable=protected-access

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
    self.call(
        'AddGroupMember',
        group_name=group_name,
        target_name=target_name,
    )

    return True

def remove_group_member(self, group_name, target_name):
    """
    This method removes a Target from the whitelist of a Group.
    """
    self.call(
        'RemoveGroupMember',
        group_name=group_name,
        target_name=target_name,
    )

    return True

def blacklist_group_member(self, group_name, target_name):
    """
    This method removes a Target from the whitelist of a Group.
    It also prevents any automember rules from including the Target.
    """
    self.call(
        'BlacklistGroupMember',
        group_name=group_name,
        target_name=target_name,
    )

    return True

def delete_group(self, name):
    """
    This method deletes a Group from the teamserver.
    """
    self.call(
        'DeleteGroup',
        name=name,
    )

    return True

def list_groups(self):
    """
    This method returns a list of Group objects on the teamserver.
    """
    resp = self._list_groups_raw() # pylint: disable=protected-access

    return [Group(group) for name, group in resp.get('groups', {}).items()]

def _list_groups_raw(self):
    """
    Returns the raw response of the ListGroups API call.
    """
    return self.call(
        'ListGroups'
    )

def add_group_rule(self, name, attribute, regex, rule_id=None):
    """
    Add an automember rule to the group.
    """
    return self.call(
        'AddGroupRule',
        name=name,
        attribute=attribute,
        regex=regex,
        rule_id=rule_id,
    )

def remove_group_rule(self, name, rule_id):
    """
    Remove an automember rule from the group.
    """
    return self.call(
        'RemoveGroupRule',
        name=name,
        rule_id=rule_id
    )

def rebuild_group_members(self, name=None):
    """
    Recalculate group members. Optionally specify a particular group.
    """
    return self.call(
        'RebuildGroupMembers',
        name=name
    )
