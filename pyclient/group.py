"""
This module contains Group API functions.
"""
from .arsenal import ArsenalObject
from .exceptions import parse_error

class Group(ArsenalObject):
    """
    This object represents a Group from the teamserver.
    """
    name = None
    whitelist_members = None
    blacklist_members = None

    @staticmethod
    def create_group(name):
        """
        This method creates a Group on the teamserver.
        """
        resp = ArsenalObject._call(
            'CreateGroup',
            name=name,)

        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def get_group(name):
        """
        This method fetches a Group object from the teamserver.
        """
        resp = ArsenalObject._call(
            'GetGroup',
            name=name,)

        if resp.get('error', True):
            parse_error(resp)

        return Group(resp.get('group'))

    @staticmethod
    def add_group_member(group_name, target_name):
        """
        This method whitelists a Target as a member of a Group.
        """
        resp = ArsenalObject._call(
            'AddGroupMember',
            group_name=group_name,
            target_name=target_name)

        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def remove_group_member(group_name, target_name):
        """
        This method removes a Target from the whitelist of a Group.
        """
        resp = ArsenalObject._call(
            'RemoveGroupMember',
            group_name=group_name,
            target_name=target_name)

        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def blacklist_group_member(group_name, target_name):
        """
        This method removes a Target from the whitelist of a Group.
        It also prevents any automember rules from including the Target.
        """
        resp = ArsenalObject._call(
            'BlacklistGroupMember',
            group_name=group_name,
            target_name=target_name)

        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def delete_group(name):
        """
        This method deletes a Group from the teamserver.
        """
        resp = ArsenalObject._call(
            'DeleteGroup',
            name=name,)

        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def list_groups():
        """
        This method returns a list of Group objects on the teamserver.
        """
        resp = ArsenalObject._call(
            'ListGroups')

        if resp.get('error', True):
            parse_error(resp)

        return [Group(group) for name, group in resp.get('groups', {}).items()]
