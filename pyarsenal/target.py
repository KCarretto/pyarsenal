"""
This module contains Target API functions.
"""
from pyarsenal.objects import Target


def create_target(self, name, uuid, facts):
    """
    This method creates a Target on the teamserver.
    """
    self.call("CreateTarget", name=name, uuid=uuid, facts=facts)

    return True


def get_target(self, name, **kwargs):
    """
    Returns a Target object from the teamserver.
    """
    resp = self._get_target_raw(name, **kwargs)  # pylint: disable=protected-access
    return Target(resp["target"])


def _get_target_raw(self, name, **kwargs):
    """
    Returns the raw response of the GetTarget API call.
    """
    return self.call(
        "GetTarget",
        name=name,
        include_status=kwargs.get("include_status", True),
        include_facts=kwargs.get("include_facts", False),
        include_sessions=kwargs.get("include_sessions", False),
        include_actions=kwargs.get("include_actions", False),
        include_groups=kwargs.get("include_groups", False),
        include_credentials=kwargs.get("include_credentials", False),
    )


def rename_target(self, name, new_name):
    """
    Renames a Target object on the teamserver.
    """
    self.call("RenameTarget", name=name, new_name=new_name)

    return True


def set_target_facts(self, name, facts):
    """
    Override Target facts with updated information.
    """
    self.call("SetTargetFacts", name=name, facts=facts)

    return True


def list_targets(self, **kwargs):
    """
    Returns a list of Target Objects from the teamserver.
    """
    resp = self._list_targets_raw(kwargs)  # pylint: disable=protected-access

    targets = [Target(target) for name, target in resp["targets"].items()]
    if kwargs.get("show_inactive"):
        targets = filter(lambda t: t.status.lower() != "active", targets)
    return targets


def _list_targets_raw(self, params):
    """
    Returns the raw response of the ListTargets API call.
    """
    return self.call(
        "ListTargets",
        include_status=params.get("include_status", True) or params.get("show_inactive"),
        include_facts=params.get("include_facts", False),
        include_sessions=params.get("include_sessions", False),
        include_actions=params.get("include_actions", False),
        include_groups=params.get("include_groups", False),
        include_credentials=params.get("include_credentials", False),
    )


def migrate_target(self, old_target, new_target):
    """
    Invoke the MigrateTarget API method.
    """
    return self.call("MigrateTarget", old_target=old_target, new_target=new_target)
