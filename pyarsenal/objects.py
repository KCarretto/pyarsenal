"""
This module contains all objects that can be created on or retrieved from the teamserver.
"""
class ArsenalObject(object): # pylint: disable=too-few-public-methods
    """
    This object contains common-purpose functions that other modules will inherit from.
    """
    raw_json = None

    def __init__(self, object_json):
        """
        This constructor takes json and sets the objects attributes accordingly.
        """
        self.raw_json = object_json
        for key, value in object_json.items():
            self.__setattr__(key, value)

    def __str__(self):
        return str(self.raw_json)

    @property
    def json(self):
        """
        Get a JSON representation of the object.
        """
        return self.raw_json

class Action(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents an Action from the teamserver.
    """
    action_id = None
    bound_session_id = None
    status = None
    target_name = None
    action_string = None

    queue_time = None
    sent_time = None
    complete_time = None

    response = None

    owner = None

class Group(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents a Group from the teamserver.
    """
    name = None
    members = None
    whitelist_members = None
    blacklist_members = None
    rules = None

class GroupAction(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents a GroupAction from the teamserver.
    """
    group_action_id = None
    action_string = None
    status = None
    action_ids = None
    actions = None
    owner = None

class Log(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents a Log from the teamserver.
    """
    timestamp = None
    application = None
    level = None
    message = None

class Session(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents a Session from the teamserver.
    """
    session_id = None
    target_name = None
    status = None
    timestamp = None
    config = None
    agent_version = 'None Specified'

class Target(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents a Target from the teamserver.
    """
    name = None
    status = None
    lastseen = None
    public_ips = None
    uuid = None
    facts = None
    sessions = None
    credentials = None
    groups = None
    actions = None


##
# Auth Objects
##
class Role(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents a Role from the teamserver.
    """
    name = None
    description = None
    allowed_api_calls = None
    users = None

class APIKey(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents an API Key from the teamserver.
    """
    key = None
    owner = None
    allowed_api_calls = None

class User(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents a User from the teamserver.
    """
    username = None
    allowed_api_calls = None
    roles = None

##
# Webhooks
##
class Webhook(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents a Webhook from the teamserver.
    """
    hook_id = None
    owner = None
    post_url = None
    triggers = None

##
# Agents
##
class Agent(ArsenalObject): # pylint: disable=too-few-public-methods
    """
    This object represents an Agent from the teamserver.
    """
    agent_version = None
    supported_actions = None
    default_config = None
