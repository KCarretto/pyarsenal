"""
This module contains GroupAction API functions.
"""
from pyarsenal.objects import Action, GroupAction

def create_group_action(self, group_name, action_string, group_action_id=None, quick=False):
    """
    This method creates an GroupAction, and returns it's group_action_id.
    """
    resp = self.call(
        'CreateGroupAction',
        group_name=group_name,
        action_string=action_string,
        group_action_id=group_action_id,
        quick=quick,
    )

    return resp['group_action_id']

def get_group_action(self, group_action_id):
    """
    This method fetches information about a GroupAction.
    """
    resp = self._get_group_action_raw(group_action_id) # pylint: disable=protected-access

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
    self.call(
        'CancelGroupAction',
        group_action_id=group_action_id
    )

    return True

def list_group_actions(self):
    """
    This method lists group actions on the teamserver.staticmethod
    """

    resp = self._list_group_actions_raw() # pylint: disable=protected-access

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
