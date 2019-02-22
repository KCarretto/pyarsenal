"""
This module contains Action API functions.
"""
from pyarsenal.objects import Action


def create_action(  # pylint: disable=too-many-arguments
    self, target_name, action_string, bound_session_id=None, action_id=None, quick=False
):
    """
    This method creates an Action, and returns it's action_id.
    """
    resp = self.call(
        "CreateAction",
        target_name=target_name,
        action_string=action_string,
        bound_session_id=bound_session_id,
        action_id=action_id,
        quick=quick,
    )

    return resp["action_id"]


def get_action(self, action_id):
    """
    Returns an Action object from the teamserver.
    """
    resp = _get_action_raw(self, action_id)

    return Action(resp["action"])


def _get_action_raw(self, action_id):
    """
    Returns the raw response of the GetAction API call.
    """
    return self.call("GetAction", action_id=action_id)


def cancel_action(self, action_id):
    """
    Attempts to cancel an Action. Returns True if successful, False otherwise.
    """
    self.call("CancelAction", action_id=action_id)

    return True


def list_actions(self, **kwargs):
    """
    Returns a list of Action Objects from the teamserver.
    """
    resp = _list_actions_raw(self, **kwargs)

    return [Action(action) for action_id, action in resp["actions"].items()]


def _list_actions_raw(self, **kwargs):
    """
    Returns the raw response of the ListActions API call.
    """
    return self.call(
        "ListActions",
        owner=kwargs.get("owner"),
        target_name=kwargs.get("target_name"),
        limit=kwargs.get("limit"),
        offset=kwargs.get("offset"),
    )


def duplicate_action(self, action_id):
    """
    Duplicate an action.
    """
    resp = self.call("DuplicateAction", action_id=action_id)
    return resp["action_id"]
