"""
This module contains GroupAction API functions.
"""
from .objects import Action, GroupAction
from .exceptions import parse_error

def create_group_action(self, group_name, action_string):
    """
    This method creates an GroupAction, and returns it's group_action_id.
    """
    resp = self.call(
        'CreateGroupAction',
        group_name=group_name,
        action_string=action_string
    )

    if resp.get('error', True):
        parse_error(resp)

    return resp['group_action_id']

def get_group_action(self, group_action_id):
    """
    This method fetches information about a GroupAction.
    """
    resp = self._get_group_action_raw(group_action_id) # pylint: disable=protected-access

    if resp.get('error', True):
        parse_error(resp)

    group_action = GroupAction(resp['group_action'])

    group_action.actions = [Action(action) for action in resp['group_action']['actions']]

    return group_action

def _get_group_action_raw(self, group_action_id):
    """
    Returns the raw response of the GetGroupAction API call.
    """
    return self.call(
        'GetGroupAction',
        group_action_id=group_action_id
    )

def cancel_group_action(self, group_action_id):
    """
    This method attempts to cancel a group action.
    """
    resp = self.call(
        'CancelGroupAction',
        group_action_id=group_action_id
    )

    if resp.get('error', True):
        parse_error(resp)

def list_group_actions(self):
    """
    This method lists group actions on the teamserver.staticmethod
    """

    resp = self._list_group_actions_raw() # pylint: disable=protected-access

    if resp.get('error', True):
        parse_error(resp)

    group_actions = []
    if resp['group_actions']:
        for _, group_action_raw in resp['group_actions'].items():
            group_action = GroupAction(group_action_raw)
            group_action.actions = [Action(action) for action in group_action_raw['actions']]
            group_actions.append(group_action)

    return group_actions

def _list_group_actions_raw(self):
    """
    Returns the raw response of the ListGroupActions API call.
    """
    return self.call(
        'ListGroupActions',
    )
