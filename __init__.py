#pylint: disable=invalid-name
"""
This package contains objects and methods for interacting with the Arsenal teamserver API.
"""
from .pyclient import Action, Group, GroupAction, Log, Session, Target
from .pyclient import ArsenalClient, API_KEY_FILE, TEAMSERVER_URI

from .pyclient import (
    APIException,
    ActionUnboundSession,
    SessionUnboundTarget,
    CannotCancelAction,
    CannotAssignAction,
    CannotBindAction,
    ActionSyntaxError,
    MembershipError,

    ValidationError,
    ResourceNotFound,
    ResourceAlreadyExists,
    MissingParameter,

    InvaidUser,
    InvalidCredentials,
    InvalidAPIKey,
    PermissionDenied,
)

from .cli import CLI
