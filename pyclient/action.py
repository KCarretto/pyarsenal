"""
This module contains Action API functions.
"""
from .exceptions import parse_error
from .objects import Action

def create_action(self, target_name, action_string, bound_session_id=None):
    """
    This method creates an Action, and returns it's action_id.
    """
    resp = self.call(
        'CreateAction',
        target_name=target_name,
        action_string=action_string,
        bound_session_id=bound_session_id)

    if resp.get('error', True):
        parse_error(resp)

    return resp['action_id']

def get_action(self, action_id):
    """
    Returns an Action object from the teamserver.
    """
    resp = _get_action_raw(self, action_id)
    if resp.get('error', True):
        parse_error(resp)

    return Action(resp['action'])

def _get_action_raw(self, action_id):
    """
    Returns the raw response of the GetAction API call.
    """
    return self.call(
        'GetAction',
        action_id=action_id)

def cancel_action(self, action_id):
    """
    Attempts to cancel an Action. Returns True if successful, False otherwise.
    """
    resp = self.call(
        'CancelAction',
        action_id=action_id
    )
    if resp.get('error', True):
        return False

    return True

def list_actions(self):
    """
    Returns a list of Action Objects from the teamserver.
    """
    resp = _list_actions_raw(self)

    if resp.get('error', True):
        parse_error(resp)

    return [Action(action) for action_id, action in resp['actions'].items()]

def _list_actions_raw(self):
    """
    Returns the raw response of the ListActions API call.
    """
    return self.call(
        'ListActions'
    )
