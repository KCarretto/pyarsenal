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

    @staticmethod
    def cancel_group_action(group_action_id):
        """
        This method attempts to cancel a group action.
        """
        resp = ArsenalObject._call(
            'CancelGroupAction',
            group_action_id=group_action_id
        )

        if resp.get('error', True):
            parse_error(resp)

    @staticmethod
    def list_group_actions():
        """
        This method lists group actions on the teamserver.staticmethod
        """
        resp = ArsenalObject._call(
            'ListGroupActions',
        )

        if resp.get('error', True):
            parse_error(resp)

        group_actions = []
        if resp['group_actions']:
            for _, group_action_raw in resp['group_actions'].items():
                group_action = GroupAction(group_action_raw)
                group_action.actions = [Action(action) for action in group_action_raw['actions']]
                group_actions.append(group_action)

        return group_actions
