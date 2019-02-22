"""
This module contains shared resources that modules in the library can use.
"""
from os.path import exists

import requests
from requests.exceptions import (
    ContentDecodingError,
    ConnectionError,
    Timeout,
)  # pylint: disable=redefined-builtin

from pyarsenal.exceptions import ServerConnectionError, ServerInternalError, parse_error

from pyarsenal.action import (
    create_action,
    get_action,
    cancel_action,
    list_actions,
    _get_action_raw,
    _list_actions_raw,
    duplicate_action,
)
from pyarsenal.group import (
    create_group,
    get_group,
    add_group_member,
    remove_group_member,
    blacklist_group_member,
    delete_group,
    list_groups,
    _get_group_raw,
    _list_groups_raw,
    add_group_rule,
    remove_group_rule,
    rebuild_group_members,
)
from pyarsenal.group_action import (
    create_group_action,
    get_group_action,
    cancel_group_action,
    list_group_actions,
    _get_group_action_raw,
    _list_group_actions_raw,
)

from pyarsenal.log import create_log, list_logs, _list_logs_raw

from pyarsenal.session import (
    create_session,
    get_session,
    session_checkin,
    update_session_config,
    list_sessions,
    _get_session_raw,
    _list_sessions_raw,
)

from pyarsenal.target import (
    create_target,
    get_target,
    set_target_facts,
    rename_target,
    list_targets,
    _get_target_raw,
    _list_targets_raw,
    migrate_target,
)

from pyarsenal.auth import (
    create_role,
    create_api_key,
    create_user,
    get_user,
    get_role,
    get_current_context,
    add_role_member,
    remove_role_member,
    update_role_permissions,
    update_user_password,
    list_users,
    list_api_keys,
    list_roles,
    delete_user,
    delete_role,
    revoke_api_key,
)

from pyarsenal.agent import register_agent, get_agent, list_agents, unregister_agent

from pyarsenal.webhook import register_webhook, unregister_webhook, list_webhooks


class ArsenalClient(object):
    """
    This object is used to invoke API functions.
    """

    context = None

    # Action API
    create_action = create_action
    get_action = get_action
    cancel_action = cancel_action
    list_actions = list_actions
    _get_action_raw = _get_action_raw
    _list_actions_raw = _list_actions_raw
    duplicate_action = duplicate_action

    # Group API
    create_group = create_group
    get_group = get_group
    add_group_member = add_group_member
    remove_group_member = remove_group_member
    blacklist_group_member = blacklist_group_member
    delete_group = delete_group
    list_groups = list_groups
    _get_group_raw = _get_group_raw
    _list_groups_raw = _list_groups_raw
    add_group_rule = add_group_rule
    remove_group_rule = remove_group_rule
    rebuild_group_members = rebuild_group_members

    # GroupAction API
    create_group_action = create_group_action
    get_group_action = get_group_action
    cancel_group_action = cancel_group_action
    list_group_actions = list_group_actions
    _get_group_action_raw = _get_group_action_raw
    _list_group_actions_raw = _list_group_actions_raw

    # Log API
    create_log = create_log
    list_logs = list_logs
    _list_logs_raw = _list_logs_raw

    # Session API
    create_session = create_session
    get_session = get_session
    session_checkin = session_checkin
    update_session_config = update_session_config
    list_sessions = list_sessions
    _get_session_raw = _get_session_raw
    _list_sessions_raw = _list_sessions_raw

    # Target API
    create_target = create_target
    get_target = get_target
    set_target_facts = set_target_facts
    rename_target = rename_target
    list_targets = list_targets
    _get_target_raw = _get_target_raw
    _list_targets_raw = _list_targets_raw
    migrate_target = migrate_target

    # Auth API
    create_role = create_role
    create_api_key = create_api_key
    create_user = create_user
    get_user = get_user
    get_role = get_role
    get_current_context = get_current_context
    add_role_member = add_role_member
    remove_role_member = remove_role_member
    update_role_permissions = update_role_permissions
    update_user_password = update_user_password
    list_users = list_users
    list_roles = list_roles
    list_api_keys = list_api_keys
    delete_user = delete_user
    delete_role = delete_role
    revoke_api_key = revoke_api_key

    # Agent API
    register_agent = register_agent
    get_agent = get_agent
    list_agents = list_agents
    unregister_agent = unregister_agent

    # Webhook API
    register_webhook = register_webhook
    unregister_webhook = unregister_webhook
    list_webhooks = list_webhooks

    def __init__(self, uri: str, api_key_file=None, username=None, password=None, **kwargs):
        """
        Create an instance of the client, which will store authentication information.

        Set the 'api_key_file' to enable using an API key
        Set the 'username' and 'password' to use user authentication otherwise.
        """
        if not uri:
            raise ServerConnectionError("Must provide a URI when building an ArsenalClient.")

        if not uri.startswith("http"):
            uri = f"http://{uri}"

        self.teamserver_uri = uri

        if api_key_file:
            if not self.api_key_exists(api_key_file):
                print(f"WARN: API key file specified but none found {api_key_file}")
            with open(api_key_file, "r") as keyfile:
                self.api_key = keyfile.readlines()[0].strip().strip("\n")
        if username and password:
            self.login_username = username
            self.login_password = password

        self.context = self.get_current_context()

    @staticmethod
    def api_key_exists(api_key_file):
        """
        Determines if the keyfile exists.
        """
        return exists(api_key_file)

    def call(self, method, **kwargs):
        """
        Helper used to call API functions.
        """
        params = {}

        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        params["method"] = method

        if hasattr(self, "api_key") and self.api_key:
            params["login_api_key"] = self.api_key
        elif hasattr(self, "login_username") and hasattr(self, "login_password"):
            params["login_username"] = self.login_username
            params["login_password"] = self.login_password
        try:
            headers = {
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "*/*",
                "User-Agent": "arsenal-api-python-client requests",
            }

            resp = requests.post(
                self.teamserver_uri, headers=headers, json=params, timeout=30
            ).json()

            if resp.get("error"):
                parse_error(resp)
            return resp
        except ContentDecodingError:
            raise ServerInternalError("Error: The teamserver encountered an unexpected error.")
        except Timeout:
            raise ServerInternalError(
                "Error: The teamserver was unable to handle the request in time."
            )
        except ConnectionError as exception:
            raise ServerConnectionError("Could not connect to the teamserver. {}".format(exception))
