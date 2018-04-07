"""
This module includes a class that contains all API functions,
and may be called from the command line.
"""
from datetime import datetime
from getpass import getpass

import colorama
import fire

try:
    # Attempt relative import, will not work if __main__
    from .pyclient import ArsenalClient, API_KEY_FILE
except Exception: #pylint: disable=broad-except
    from pyclient import ArsenalClient, API_KEY_FILE

class CLI(object): #pylint: disable=too-many-public-methods
    """
    This class contains all user API functions.
    It may be invoked using the Google Python Fire library by running it from the command line.
    """
    client = None
    _output_lines = []
    _color = True
    _display_output = True

    def __init__(self, **kwargs):
        """
        Constructor arguments:
        enable_color: Should special characters to enable color be inserted into the output?
        display_output: Should output be printed to stdout
        api_key_file: The location of the API key file.
        username: The username to authenticate with (not required if api_key_file is specified).
        password: The password to authenticate with (not required if api_key_file is specified).

        If api_key_file, username, and password are not specified, the user is prompted to input
        the username and password.
        """
        self._display_output = kwargs.get('display_output', True)
        self._color = kwargs.get('enable_color', True)

        api_key_file = kwargs.get('api_key_file')
        if ArsenalClient.api_key_exists(api_key_file):
            self.client = ArsenalClient(
                api_key_file=api_key_file
            )
        else:
            self.username = kwargs.get('username')
            self.password = kwargs.get('password')
            if not self.username or not self.password:
                self.username = input("Username: ")
                self.password = getpass("Password: ")
            self.client = ArsenalClient(
                username=self.username,
                password=self.password,
            )
        self._output_lines = []

    ###############################################################################################
    #                                   Utility Methods                                           #
    ###############################################################################################

    def _output(self, msg):
        """
        Display a message. Also add it to the output_lines field, for programmatic access.
        """
        self._output_lines.append(msg)
        print(msg)

    # Helper functions
    # Color Scheme:
        # Keys - Cyan
        # Data - Normal
        # Identifiers - Blue
        # Actions strings - Yellow

    def _purple(self, msg):
        return '{}{}{}'.format(
            colorama.Fore.MAGENTA, msg, colorama.Fore.RESET) if self._color else msg

    def _blue(self, msg):
        return '{}{}{}'.format(
            colorama.Fore.BLUE, msg, colorama.Fore.RESET) if self._color else msg

    def _cyan(self, msg):
        return '{}{}{}'.format(
            colorama.Fore.CYAN, msg, colorama.Fore.RESET) if self._color else msg

    def _green(self, msg):
        return '{}{}{}'.format(
            colorama.Fore.GREEN, msg, colorama.Fore.RESET) if self._color else msg

    def _yellow(self, msg):
        return '{}{}{}'.format(
            colorama.Fore.YELLOW, msg, colorama.Fore.RESET) if self._color else msg

    def _red(self, msg):
        return '{}{}{}'.format(
            colorama.Fore.RED, msg, colorama.Fore.RESET) if self._color else msg

    def _id(self, msg):
        return '{}{}{}'.format(
            colorama.Fore.BLUE, msg, colorama.Fore.RESET) if self._color else msg

    def _key(self, msg):
        return '{}{}{}'.format(
            colorama.Fore.CYAN, msg, colorama.Fore.RESET,
        ) if self._color else msg

    def _pair(self, key, value, value_func=None):
        if not self._color:
            return '{0:<25}: {1:<30}'.format(key, value)

        if value_func and callable(value_func):
            return '{0:<25}: {1:<30}'.format(
                self._key(key),
                value_func(value)
            )

        return '{0:<25}: {1:<30}'.format(
            self._key(key),
            value
        )

    def _bright(self, msg):
        return '{}{}{}'.format(
            colorama.Style.BRIGHT, msg, colorama.Style.RESET_ALL
        ) if self._color else msg

    def _format_action_status(self, status):
        if status == 'queued':
            status = self._purple(status)
        elif status == 'sent':
            status = self._blue(status)
        elif status == 'complete':
            status = self._green(status)
        elif status == 'stale' or status == 'failing':
            status = self._yellow(status)
        else:
            status = self._red(status)

        return status

    def _format_group_action_status(self, status):
        if status == 'queued':
            status = self._purple(status)
        elif status == 'in-progress':
            status = self._cyan(status)
        elif status == 'mixed success':
            status = self._yellow(status)
        elif status == 'success':
            status = self._green(status)
        else:
            status = self._red(status)

        return status

    def _format_session_status(self, status):
        if status == 'active':
            status = self._green(status)
        elif status == 'missing':
            status = self._yellow(status)
        else:
            status = self._red(status)

        return status

    def _format_loglevel(self, level):
        loglevel = level.lower()
        if loglevel == 'debug':
            level = self._purple(level)
        elif loglevel == 'info':
            level = self._green(level)
        elif loglevel == 'warn':
            level = self._yellow(level)
        else:
            level = self._red(level)
        return level

    def _format_facts(self, facts, indent=8):
        format_str = ''
        i = ' '*indent
        for key, value in facts.items():
            if isinstance(value, dict):
                format_str = '{}\n{}{}: {}'.format(
                    format_str, i, self._key(key), self._format_facts(value, indent*2))
            elif isinstance(value, list):
                if value:
                    if isinstance(value[0], dict):
                        format_str = '{}\n{}{}:'.format(format_str, i, self._key(key))
                        for subval in value:
                            format_str = '{}\n{}{}'.format(
                                format_str,
                                i,
                                self._format_facts(subval, indent*2))
                    else:
                        format_str = '{}\n{}{}: {}'.format(
                            format_str, i, self._key(key), value)
                else:
                    format_str = '{}\n{}{}: {}'.format(
                        format_str, i, self._key(key), '[]'
                    )
            else:
                format_str = '{}\n{}{}: {}'.format(
                    format_str, i, self._key(key), value
                )
        return format_str

    ###############################################################################################
    #                              Help Methods                                                   #
    ###############################################################################################

    def help(self, api_method=None):
        """
        Display API help for a given API method.

        You may request additional information by running help <Method Name>

        Args:
            api_method: The name of the API method.
        """
        if api_method is None:
            self._output('\nAvailable methods:\n')
            methods = self.client.context.allowed_api_calls
            if '*' in methods:
                methods = filter(lambda x: not x.startswith('_'), dir(self))

            self._output('\n'.join(sorted(methods)))
            return

        try:
            self._output(self.__getattribute__(api_method).__doc__)
        except AttributeError:
            self._output(self._red('Invalid method.'))

    ###############################################################################################
    #                              Action Methods                                                 #
    ###############################################################################################
    def CreateAction(self, target_name, action_string, bound_session_id=None): #pylint: disable=invalid-name
        """
        This method creates an Action for the given Target.

        Args:
            target_name: The name identifier of the Target to create an Action for.
            action_string: The Action to perform, which should conform to Arsenal Action Syntax.
            bound_session_id(optional): This parameter can be used to ensure that only a specific
                                        session may retrieve the action.
        """
        action_id = self.client.create_action(target_name, action_string, bound_session_id)
        self._output('Action created. \
        You can track it\'s progress using this action_id: `{}`'.format(self._id(action_id)))

    def GetAction(self, action_id): #pylint: disable=invalid-name
        """
        This method fetches an Action from the teamserver.

        Args:
            action_id: The identifier of the Action to fetch.
        """
        action = self.client.get_action(action_id)

        self._output(self._green('\nAction Found:\n'))
        self._output(self._pair('\taction_id', action.action_id, self._id))
        self._output(self._pair('\ttarget', action.target_name, self._id))
        self._output(self._pair('\tstatus', action.status, self._format_action_status))
        self._output(self._pair('\taction', action.action_string, self._yellow))

        if action.response:
            stdout = action.response.get('stdout')
            stderr = action.response.get('stderr')
            if stdout:
                self._output(self._pair('\tstdout', '\n{}'.format(stdout), self._green))
            if stderr:
                self._output(self._pair('\tstderr', '\n{}'.format(stderr), self._red))

    def CancelAction(self, action_id): #pylint: disable=invalid-name
        """
        This attempts to cancel an Action.

        Args:
            action_id: The identifier of the action to fetch.
        """
        cancelled = self.client.cancel_action(action_id)

        if cancelled:
            self._output(
                self._green('Action `{}` successfully cancelled.'.format(self._id(action_id))))
        else:
            self._output(
                self._red('Could not cancel Action `{}`.'.format(self._id(action_id))))

    def ListActions(self): #pylint: disable=invalid-name
        """
        This lists all Actions that are currently tracked by the teamserver.

        Args:
            None
        """
        actions = self.client.list_actions()

        if actions:
            self._output(self._bright('\n{0:<40}{1:<20}{2:<40}{3:<40}').format(
                'Target',
                'Status',
                'Action ID',
                'Action String'))
            for action in actions:
                self._output('{0:<50}{1:<30}{2:<50}{3:50}'.format(
                    self._id(action.target_name),
                    self._format_action_status(action.status),
                    self._id(action.action_id),
                    self._yellow(action.action_string),
                    ))
        else:
            self._output(self._red('No Actions were found.'))

    ###############################################################################################
    #                              Session Methods                                                #
    ###############################################################################################
    def GetSession(self, session_id): #pylint: disable=invalid-name
        """
        This method fetches an Session from the teamserver.

        Args:
            session_id: The identifier of the Session to fetch.
        """
        session = self.client.get_session(session_id)
        lastseen = datetime.fromtimestamp(session.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        self._output(self._green('\nSession Found:\n'))
        self._output(self._pair('\tsession_id', session.session_id, self._id))
        self._output(self._pair('\ttarget', session.target_name, self._yellow))
        self._output(self._pair('\tstatus', session.status, self._format_session_status))
        self._output(self._pair('\tLast Seen', lastseen))
        self._output(self._pair('\tconfig', self._format_facts(session.config)))

    def ListSessions(self, sortby='target_name'): #pylint: disable=invalid-name
        """
        This lists all Sessions that are currently tracked by the teamserver.

        Args:
            None
        """
        sessions = self.client.list_sessions()
        if sessions:
            self._output(self._bright('\n{0:<40}{1:<20}{2:<40}').format(
                'Target', 'Status', 'Session'))
            for session in sorted(sessions, key=lambda x: x.raw_json.get(sortby, 0)):
                self._output('{0:<50}{1:<30}{2:<50}'.format(
                    self._id(session.target_name),
                    self._format_session_status(session.status),
                    self._id(session.session_id),
                    ))
        else:
            self._output(self._red('No Sessions were found.'))
    ###############################################################################################
    #                               Target Methods                                                #
    ###############################################################################################
    def GetTarget(self, name, show_facts=False, hide_actions=False): #pylint: disable=invalid-name
        """
        Fetch information about a Target.

        Args:
            name: The name of the Target to search for.
            show-facts: Set True to display all facts
        """
        target = self.client.get_target(
            name,
            include_status=True,
            include_groups=True,
            include_actions=not hide_actions,
            include_facts=True)

        if target:
            lastseen = datetime.fromtimestamp(target.lastseen).strftime('%Y-%m-%d %H:%M:%S')
            groups = [group.get('name') for group in target.groups]
            self._output(self._green('\nTarget Found:\n'))
            self._output(self._pair('\tname', target.name, self._id))
            self._output(self._pair('\tstatus', target.status, self._format_session_status))
            self._output(self._pair('\tlast seen', lastseen, self._yellow))
            self._output(self._pair('\tgroups', ', '.join(groups), self._id))
            self._output('\n')
            self._output(self._pair('\thostname', target.facts.get('hostname', 'unknown hostname')))

            ip_addrs = []
            for iface in target.facts.get('interfaces', []):
                addrs = iface.get('ip_addrs')
                if addrs:
                    for addr in addrs:
                        if addr != '127.0.0.1' and not addr.startswith('169.254'):
                            ip_addrs.append(addr)
            self._output(self._pair('\tIP Addresses', ', '.join(sorted(ip_addrs))))

            if not hide_actions:
                if target.actions:
                    self._output('\n\nActions:')

                    actions = sorted(
                        target.actions,
                        key=lambda x: x.get('queue_time', 0),
                        reverse=True)

                    for action in actions:
                        self._output(self._pair('\taction_id', action.get('action_id'), self._id))
                        self._output(
                            self._pair('\taction', action.get('action_string'), self._yellow))
                        self._output(
                            self._pair(
                                '\tstatus',
                                action.get('status'),
                                self._format_action_status))
                        self._output('\n')

            if show_facts:
                self._output('\nAll Facts:')
                self._output('\t{}'.format(self._format_facts(target.facts)))
        else:
            self._output(self._red('Target not found.'))

    def RenameTarget(self, name, new_name): #pylint: disable=invalid-name
        """
        This renames a target with the given name, to the new_name.

        Args:
            name: The current name of the target.
            new_name: The desired name of the target.
        """
        self.client.rename_target(name, new_name)
        self._output(self._green('Target renamed successfully.'))

    def ListTargets(self): #pylint: disable=invalid-name
        """
        This lists all Targets that are currently tracked by the teamserver.

        Args:
            None
        """
        targets = self.client.list_targets(
            include_status=True,
            include_facts=False,
            include_actions=False,
            include_sessions=False,
            include_groups=True,
            include_credentials=False)
        if targets:
            self._output(self._bright('\n{0:<20}{1:<40}{2:<40}').format(
                'Status',
                'Name',
                'Groups'))
            for target in sorted(targets, key=lambda x: x.name):
                groups = [group['name'] for group in target.groups]
                self._output('{0:<30}{1:<50}{2:<50}'.format(
                    self._format_session_status(target.status),
                    self._id(target.name),
                    self._green(', '.join(groups) if groups else 'None')
                ))
        else:
            self._output(self._red('No Targets were found.'))

    ###############################################################################################
    #                                   Group Methods                                             #
    ###############################################################################################
    def CreateGroup(self, name): #pylint: disable=invalid-name
        """
        Create a Group of Targets.

        Args:
            name: The name of the Group.
        """
        self.client.create_group(name)
        self._output(self._green('Successfully created group: {}'.format(name)))

    def GetGroup(self, name): #pylint: disable=invalid-name
        """
        Fetch information about a Group.

        Args:
            name: The name of the Group.
        """
        group = self.client.get_group(name)
        self._output(self._pair('\tname', group.name, self._id))
        self._output(self._pair(
            '\tmembers',
            ', '.join(group.whitelist_members) if group.whitelist_members else 'None'))

        if group.blacklist_members:
            self._output(self._pair(
                '\tblacklist',
                ', '.join(group.blacklist_members),
                self._red))

    def AddGroupMember(self, group_name, target_name): #pylint: disable=invalid-name
        """
        Add a Target to a Group's whitelist.

        Args:
            group_name: The name of the Group to modify.
            target_name: The name of the Target to add to the Group.
        """
        self.client.add_group_member(group_name, target_name)
        self._output(self._green('Successfully added member to group.'))

    def RemoveGroupMember(self, group_name, target_name): #pylint: disable=invalid-name
        """
        Remove a Target from a Group's whitelist.

        Args:
            group_name: The name of the Group to modify.
            target_name: The name of the Target to remove from the Group.
        """
        self.client.remove_group_member(group_name, target_name)
        self._output(self._green('Successfully remove member from group.'))

    def BlacklistGroupMember(self, group_name, target_name): #pylint: disable=invalid-name
        """
        Remove a Target from a Group's whitelist and prevent it from being included
        as a part of an automember rule.

        Args:
            group_name: The name of the Group to modify.
            target_name: The name of the Target to add to the Group.
        """
        self.client.blacklist_group_member(group_name, target_name)
        self._output(self._green('Successfully blacklisted member from group.'))

    def ListGroups(self): #pylint: disable=invalid-name
        """
        List all Groups on the teamserver.

        Args:
            None
        """
        groups = self.client.list_groups()
        if groups:
            self._output(self._green('Groups:\n'))
            for group in groups:
                self._output('\t{}'.format(group.name))
        else:
            self._output(self._red('No Groups available.'))

    def DeleteGroup(self, name): #pylint: disable=invalid-name
        """
        Delete a group from the teamserver.

        Args:
            name: The name of the Group to delete.
        """
        self.client.delete_group(name)
        self._output(self._green('Successfully deleted group.'))

    ###############################################################################################
    #                             Group Action Methods                                            #
    ###############################################################################################
    def CreateGroupAction(self, group_name, action_string): #pylint: disable=invalid-name
        """
        Queue an Action for a Group of Targets.

        Args:
            group_name: The name of the Group of Targets.
            action_string: The Arsenal-Syntax action string to executes.
        """
        group_action_id = self.client.create_group_action(group_name, action_string)
        self._output('Action created. You can track it\'s progress using \
        this group_action_id: `{}`'.format(self._id(group_action_id)))

    def GetGroupAction(self, group_action_id): #pylint: disable=invalid-name
        """
        Fetch information about a Group Action from the teamserver.

        Args:
            group_action_id: The identifier of group action.
        """
        group_action = self.client.get_group_action(group_action_id)

        self._output('\n{}\n'.format(self._pair(
            '\t{}'.format(group_action.group_action_id),
            group_action.action_string,
            self._yellow)))
        self._output(self._pair('\tstatus', group_action.status, self._format_group_action_status))

        if group_action.actions:
            for action in group_action.actions:
                self._output('[{}]\t{}\t{}'.format(
                    self._format_action_status(action.status),
                    action.target_name,
                    action.action_id))

    def CancelGroupAction(self, group_action_id): #pylint: disable=invalid-name
        """
        Attempt to cancel a group action. This will only work for targets that have not
        yet had the action sent to a session.

        Args:
            group_action_id: The identifier of group action.
        """
        self.client.cancel_group_action(group_action_id)
        self._output(self._green('Successfully cancelled GroupAction'))

    def ListGroupActions(self): #pylint: disable=invalid-name
        """
        List all Group Actions.

        Args:
            None
        """
        group_actions = self.client.list_group_actions()
        if group_actions:
            self._output(self._bright('\n{0:<20}{1:<40}{2:<40}').format('Status', 'ID', 'Action'))
            for group_action in group_actions:
                self._output('{0:<30}{1:<50}{2:<50}'.format(
                    self._format_group_action_status(group_action.status),
                    self._id(group_action.group_action_id),
                    self._yellow(group_action.action_string)))
        else:
            self._output(self._red('No GroupActions available.'))
    ###############################################################################################
    #                                 Log Methods                                                 #
    ###############################################################################################
    def ListLogs(self, application=None, since=None, include_archived=None):  #pylint: disable=invalid-name
        """
        This lists logs from the teamserver, and may be optionally filtered.

        Args:
            application(optional): The Application to filter for.
            since(optional): All logs returned will have a timestamp greater than this.
            include_archived(optional): Should archived logs be included in the search.
        """
        logs = self.client.list_logs(application, since, include_archived)
        for log in logs:
            timestamp = datetime.fromtimestamp(log.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            self._output('[{}][{}]\t[{}]\t{}'.format(
                timestamp,
                self._blue(log.application),
                self._format_loglevel(log.level),
                log.message
            ))

    ###############################################################################################
    #                                 Auth Methods                                                #
    ###############################################################################################
    def CreateUser(self, username=None, password=None): #pylint: disable=invalid-name
        """
        This creates a user.

        Args:
            username: The username for the new user, must not already exist.
            password: The password for the new user.

            If the arguments are not specified, you will be prompted to enter them securely.
        """
        if not username:
            username = input('Username: ')
        if not password:
            password = getpass('Password: ')
            confirm = getpass('Confirm Password: ')
            if password != confirm:
                self._output(self._red('Passwords did not match'))
                return
        self.client.create_user(username, password)
        self._output(self._green('Successfully created user: {}'.format(username)))

    def CreateAPIKey(self, allowed_api_calls=None, user_context=None): #pylint: disable=invalid-name
        """
        Generate an API key for the user. Optionally limit it's permissions by supplying a list
        of allowed api calls for it. By default, the API key will assume all permissions of the
        current user.

        Args:
            allowed_api_calls:  A list of allowed API calls
                                defaults to all calls accessible by the user.
                                i.e. CreateAPIKey "['GetCurrentContext', 'ListTargets']"

        Administrators may specify another user to create a key for using 'user_context'.
        """
        key = self.client.create_api_key(allowed_api_calls, user_context)

        self._output(self._pair(self._green('Successfully generated API Key'), key, self._yellow))

    def CreateRole(self, role_name, allowed_api_calls, users):  #pylint: disable=invalid-name
        """
        Create a role with the given permissions and users.

        Args:
            role_name: The name of the role.
            allowed_api_calls: A list of methods that users in the role will be able to call.
            users: A list of users to add to the role.
        """
        self.client.create_role(role_name, allowed_api_calls, users)
        self._output(self._green('Successfully created role.'))

    def GetUser(self, username): #pylint: disable=invalid-name
        """
        Fetch information about a user from the teamserver.

        Args:
            username: The user to retrieve from the teamserver.
        """
        user = self.client.get_user(username, True, True)

        self._output(self._pair('\tName', user.username, self._id))
        self._output(self._pair(
            '\tRoles',
            ', '.join(role['name'] for role in user.roles),
            self._yellow))
        self._output('\nAllowed API Methods:')
        for method in user.allowed_api_calls:
            self._output('\t{}'.format(method))

    def GetRole(self, role_name):  #pylint: disable=invalid-name
        """
        Fetch a role from the teamserver.

        Args:
            role_name: The name of the role to retrieve information on.
        """
        role = self.client.get_role(role_name)
        desc = role.description if role.description else 'None'
        methods = '\n\t'.join(role.allowed_api_calls) if role.allowed_api_calls else 'None'
        users = '\n\t'.join(role.users if role.users else 'None')

        self._output(self._pair('\nName', role.name, self._id))
        self._output(self._pair('Description', desc))
        self._output(self._pair('Allowed API Calls\n\t', methods))
        self._output(self._pair('Users\n', users, self._id))

    def GetCurrentContext(self): #pylint: disable=invalid-name
        """
        Return information about your current operating context, including your user and
        permissions.
        """
        context = self.client.context
        self._output(self._pair('\nUser', context.username, self._yellow))
        self._output('\nAllowed Methods:\n\t')
        self._output('\n\t'.join(context.allowed_api_calls))

    def UpdateRolePermissions( #pylint: disable=invalid-name
            self,
            role_name,
            allowed_api_calls):
        """
        Override a Role's permissions with a new list.

        Args:
            role_name: The name of the role to modify.
            allowed_api_calls: A list of API calls to allow.

        i.e. UpdateRolePermissions 'attacker' "['CreateTarget']"
        """
        self.client.update_role_permissions(role_name, allowed_api_calls)
        self._output(self._green('Successfully modified role permissions.'))

    def UpdateUserPassword( #pylint: disable=invalid-name
            self,
            current_password=None,
            new_password=None,
            user_context=None):
        """
        This updates the current user's password.

        Args:
            current_password: The current password for the user.
            new_password: The desired password for the user.

            If the arguments are not specified, you will be prompted to enter them securely.

        Administrators may specify another user to create a key for using 'user_context'.
        """
        if not current_password:
            current_password = getpass('Current Password: ')
        if not new_password:
            new_password = getpass('New Password: ')
            confirm = getpass('Confirm New Password: ')
            if new_password != confirm:
                self._output(self._red('Passwords did not match'))
                return

        self.client.update_user_password(current_password, new_password, user_context)

        if hasattr(self.client, 'login_password') and self.client.login_password:
            self.client.login_password = new_password

        self._output(self._green('Successfully updated password.'))

    def AddRoleMember(self, role_name, username): #pylint: disable=invalid-name
        """
        Add the user to the given role.

        Args:
            role_name: The name of the role to modify.
            username: The name of the user to add.
        """
        self.client.add_role_member(role_name, username)

        self._output(self._green('Successfully added user to role.'))

    def RemoveRoleMember(self, role_name, username):  #pylint: disable=invalid-name
        """
        Remove the user from the given role.

        Args:
            role_name: The name of the role to modify.
            username: The name of the user to remove.
        """
        self.client.remove_role_member(role_name, username)

        self._output(self._green('Successfully removed user from role.'))

    def ListUsers(self): #pylint: disable=invalid-name
        """
        List all users and describe what roles they are in.
        """
        users = self.client.list_users(True, False)

        self._output(self._bright('\n{:<40}{:<40}').format(
            'User',
            'Roles',
        ))
        for user in users:
            roles = user.roles
            self._output('{:<50}{:<50}'.format(
                self._id(user.username),
                self._yellow(', '.join([role['name'] for role in roles] if roles else ['None'])),
            ))

    def ListRoles(self):  #pylint: disable=invalid-name
        """
        List all roles.
        """
        roles = self.client.list_roles()
        self._output(self._bright('\nRoles:'))
        for role in roles:
            self._output(
                self._id(role.name))

    def ListAPIKeys(self, user_context=None): #pylint: disable=invalid-name
        """
        List all api keys for the current user.

        Administrators may specify another user to list keys for using 'user_context'.
        """
        keys = self.client.list_api_keys(user_context)


        self._output(self._bright(''))
        for key in keys:
            allowed_api_calls = (
                ','.join(key.allowed_api_calls) if key.allowed_api_calls else 'None')
            self._output(self._pair(key.owner, allowed_api_calls))

    def DeleteUser(self, username): #pylint: disable=invalid-name
        """
        Delete a user.

        Args:
            username: The name of the user.
        """
        self.client.delete_user(username)
        self._output(self._green('Successfully deleted user'))

    def DeleteRole(self, role_name): #pylint: disable=invalid-name
        """
        Delete a role.

        Args:
            role_name: The name of the role.
        """
        self.client.delete_role(role_name)
        self._output(self._green('Successfully deleted role'))

    def RevokeAPIKey(self, api_key, user_context=None): #pylint: disable=invalid-name
        """
        Revoke an API Key.

        Args:
            api_key: The API Key to revoke. You must own this key.

        Administrators may specify another user to revoke keys for using 'user_context'.
        """
        self.client.revoke_api_key(api_key, user_context)
        self._output(self._green('Successfully revoked API key'))

    ###############################################################################################
    #                                 Agent Methods                                               #
    ###############################################################################################
    def RegisterAgent(self, agent_version, supported_actions): #pylint: disable=invalid-name
        """
        Register an agent version with the teamserver. This prevents sessions from receiving
        unsupported action types. This will update and override existing agents.

        Args:
            agent_version: The agent_version string that the agent will supply to the teamserver.
            supported_actions: A list of supported action types for this agent.

        i.e. RegisterAgent myagent "[0, 1, 3, 6]"
        """
        self.client.register_agent(agent_version, supported_actions)
        self._output(self._green('Successfully registered agent.'))

    def GetAgent(self, agent_version): #pylint: disable=invalid-name
        """
        Fetch information about an agent.

        Args:
            agent_version: The agent version string to search for.
        """
        agent = self.client.get_agent(agent_version)
        self._output(self._pair('\nAgent Version', agent.agent_version, self._id))
        self._output(self._pair('\nSupported Actions', str(agent.supported_actions)))

    def ListAgents(self): #pylint: disable=invalid-name
        """
        List all registered agents.
        """
        agents = self.client.list_agents()
        self._output('\nAgents:')
        for agent in agents:
            self._output(self._id(agent.agent_version))

    def UnregisterAgent(self, agent_version): #pylint: disable=invalid-name
        """
        Unregister an agent.

        Args:
            agent_version: The agent_version string to unregister.
        """
        self.client.unregister_agent(agent_version)
        self._output(self._green('Agent was successfuly unregistered.'))

    ###############################################################################################
    #                               Webhook Methods                                               #
    ###############################################################################################
    def RegisterWebhook(self, post_url, event_triggers): #pylint: disable=invalid-name
        """
        Hook an API call or other event, and receive information from the event.
        Useful for developing integrations.

        Args:
            post_url: The URL that data should be sent via an HTTP POST request.
            event_triggers: A list of events to subscribe to.
        """
        self.client.register_webhook(post_url, event_triggers)
        self._output(self._green('Successfully registered webhook.'))

    def UnregisterWebhook(self, hook_id): #pylint: disable=invalid-name
        """
        Unregister a webhook owned by the current user.

        Args:
            hook_id: The id of the hook to unregister. Must be owned by the current user.
        """
        self.client.unregister_webhook(hook_id)
        self._output(self._green('Successfully unregistered webhook.'))

    def ListWebhooks(self, user_context=None): #pylint: disable=invalid-name
        """
        Return a list of the current users webhooks.

        Administrators may specify an administrative user context.
        """
        webhooks = self.client.list_webhooks(user_context)
        self._output('\nWebhooks:')
        for hook in webhooks:
            self._output(self._pair('\nHook ID', hook.hook_id, self._id))
            self._output(self._pair('Owner', hook.owner))
            self._output(self._pair('Post URL', hook.post_url))
            self._output(self._pair('Triggers', ', '.join(hook.triggers)))

def main():
    """
    A main entry point for executing this file as a script.
    """
    cli = CLI(api_key_file=API_KEY_FILE)
    fire.Fire(cli)

if __name__ == '__main__':
    main()
