"""
This module contains GroupAction API functions.
"""
from .arsenal import ArsenalObject
from .action import Action
from .exceptions import parse_error

class GroupAction(ArsenalObject):
    """
    This object represents a GroupAction from the teamserver.
    """
    group_action_id = None
    action_string = None
    status = None
    action_ids = None
    actions = None

    @staticmethod
    def create_group_action(group_name, action_string):
        """
        This method creates an GroupAction, and returns it's group_action_id.
        """
        resp = ArsenalObject._call(
            'CreateGroupAction',
            group_name=group_name,
            action_string=action_string
        )

        if resp.get('error', True):
            parse_error(resp)

        return resp['group_action_id']

    @staticmethod
    def get_group_action(group_action_id):
        """
        This method fetches information about a GroupAction.
        """
        resp = ArsenalObject._call(
            'GetGroupAction',
            group_action_id=group_action_id
        )

        if resp.get('error', True):
            parse_error(resp)

        group_action = GroupAction(resp['group_action'])

        group_action.actions = [Action(action) for action in resp['group_action']['actions']]

        return group_action
