"""
This module contains Action API functions.
"""
from .arsenal import ArsenalObject
from .exceptions import parse_error

class Action(ArsenalObject):
    """
    This object represents an Action from the teamserver.
    """

    action_id = None
    status = None
    target_name = None
    action_string = None

    queue_time = None
    sent_time = None
    complete_time = None

    response = None

    @staticmethod
    def create_action(target_name, action_string, bound_session_id=None):
        """
        This method creates an Action, and returns it's action_id.
        """
        resp = ArsenalObject._call(
            'CreateAction',
            target_name=target_name,
            action_string=action_string,
            bound_session_id=bound_session_id)

        if resp.get('error', True):
            parse_error(resp)

        return resp['action_id']

    @staticmethod
    def get_action(action_id):
        """
        Returns an Action object from the teamserver.
        """
        resp = Action._get_action_raw(action_id)
        if resp.get('error', True):
            parse_error(resp)

        return Action(resp['action'])

    @staticmethod
    def _get_action_raw(action_id):
        """
        Returns the raw response of the GetAction API call.
        """
        return ArsenalObject._call(
            'GetAction',
            action_id=action_id)

    @staticmethod
    def cancel_action(action_id):
        """
        Attempts to cancel an Action. Returns True if successful, False otherwise.
        """
        resp = ArsenalObject._call(
            'CancelAction',
            action_id=action_id
        )
        if resp.get('error', True):
            return False

        return True

    @staticmethod
    def list_actions():
        """
        Returns a list of Action Objects from the teamserver.
        """
        resp = Action._list_actions_raw()

        if resp.get('error', True):
            parse_error(resp)

        return [Action(action) for action_id, action in resp['actions'].items()]

    @staticmethod
    def _list_actions_raw():
        """
        Returns the raw response of the ListActions API call.
        """
        return ArsenalObject._call(
            'ListActions'
        )
