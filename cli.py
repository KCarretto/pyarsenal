"""
This module includes a class that contains all API functions,
and may be called from the command line.
"""
from pprint import pformat
from datetime import datetime

import time
import colorama
import fire

try:
    # Attempt relative import, will not work if __main__
    from .pyclient import Action, Session, Target, Log
    from .pyclient.exceptions import handle_exceptions
except ImportError:
    from pyclient import Action, Session, Target, Log
    from pyclient.exceptions import handle_exceptions

class ArsenalClient(object):
    """
    This class contains all API functions.
    It may be invoked using the Google Python Fire library by running it from the command line.
    """
    _output_lines = []
    _color = True
    _display_output = True

    def __init__(self, enable_color=True, display_output=True):
        self._output_lines = []
        self._color = enable_color
        self._display_output = display_output

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
                    format_str, i, key, self._format_facts(value, indent*2))
            elif isinstance(value, list):
                if value:
                    if isinstance(value[0], dict):
                        for subval in value:
                            format_str = '{}\n{}{}: {}'.format(
                                format_str, i, key, self._format_facts(subval, indent*2))
                    else:
                        format_str = '{}\n{}{}: {}'.format(
                            format_str, i, key, value)
                else:
                    format_str = '{}\n{}{}: {}'.format(
                        format_str, i, key, '[]'
                    )
            else:
                format_str = '{}\n{}{}: {}'.format(
                    format_str, i, key, value
                )
        return format_str

    ###############################################################################################
    #                              Help Methods                                                   #
    ###############################################################################################

    def help(self, api_method=None):
        """
        Display API help for a given API method.

        Args:
            api_method: The name of the API method.
        """
        if api_method is None:
            self._output('\nAvailable methods:\n')
            self._output('\n'.join(sorted(filter(lambda x: not x.startswith('_'), dir(self)))))
            return

        try:
            self._output(self.__getattribute__(api_method).__doc__)
        except AttributeError:
            self._output('Invalid method.')

    ###############################################################################################
    #                              Action Methods                                                 #
    ###############################################################################################
    @handle_exceptions
    def CreateAction(self, target_name, action_string, bound_session_id=None): #pylint: disable=invalid-name
        """
        This method creates an Action for the given Target.

        Args:
            target_name: The name identifier of the Target to create an Action for.
            action_string: The Action to perform, which should conform to Arsenal Action Syntax.
            bound_session_id(optional): This parameter can be used to ensure that only a specific
                                        session may retrieve the action.
        """
        action_id = Action.create_action(target_name, action_string, bound_session_id)
        self._output('Action created. \
        You can track it\'s progress using this action_id: `{}`'.format(action_id))

    @handle_exceptions
    def GetAction(self, action_id): #pylint: disable=invalid-name
        """
        This method fetches an Action from the teamserver.

        Args:
            action_id: The identifier of the Action to fetch.
        """
        action = Action.get_action(action_id)
        status = self._format_action_status(action.status.lower())

        self._output(self._green('Action Found:\n'))
        self._output('\taction_id: {}'.format(self._blue(action.action_id)))
        self._output('\ttarget: {}'.format(action.target_name))
        self._output('\tstatus: {}'.format(status))
        self._output('\taction: {}'.format(self._yellow(action.action_string)))

        if action.response:
            stdout = action.response.get('stdout')
            stderr = action.response.get('stderr')
            if stdout:
                self._output('stdout:\n{}\n'.format(self._green(stdout)))
            if stderr:
                self._output('stderr:\n{}\n'.format(self._red(stderr)))

    @handle_exceptions
    def CancelAction(self, action_id): #pylint: disable=invalid-name
        """
        This attempts to cancel an Action.

        Args:
            action_id: The identifier of the action to fetch.
        """
        cancelled = Action.cancel_action(action_id)

        if cancelled:
            self._output(self._green('Action `{}` successfully cancelled.'.format(action_id)))
        else:
            self._output(self._red('Could not cancel Action `{}`.'.format(action_id)))

    @handle_exceptions
    def ListActions(self): #pylint: disable=invalid-name
        """
        This lists all Actions that are currently tracked by the teamserver.

        Args:
            None
        """
        actions = Action.list_actions()

        if actions:
            for action in actions:
                self._output('[{}][{}]\t{} (Target: {})'.format(
                    self._format_action_status(action.status),
                    self._blue(action.action_id),
                    self._yellow(action.action_string),
                    action.target_name))
        else:
            self._output(self._red('No Actions were found.'))

    ###############################################################################################
    #                              Session Methods                                                #
    ###############################################################################################
    @handle_exceptions
    def GetSession(self, session_id): #pylint: disable=invalid-name
        """
        This method fetches an Session from the teamserver.

        Args:
            session_id: The identifier of the Session to fetch.
        """
        session = Session.get_session(session_id)

        self._output(self._green('Session Found:\n'))
        self._output('\ttarget: {}'.format(self._yellow(session.target_name)))
        self._output('\tstatus: {}'.format(self._format_session_status(session.status)))
        self._output('\tLast Seen: {}s ago'.format(time.time() - session.timestamp))
        self._output('\tconfig:')
        self._output(pformat(session.config))
        self._output('\n\n\tsession_id: {}'.format(self._blue(session.session_id)))

    @handle_exceptions
    def ListSessions(self, sortby='target_name'): #pylint: disable=invalid-name
        """
        This lists all Sessions that are currently tracked by the teamserver.

        Args:
            None
        """
        sessions = Session.list_sessions()
        if sessions:
            for session in sorted(sessions, key=lambda x: x.raw_json.get(sortby, 0)):
                self._output('[{}]\t[{}]\t (Target: {})'.format(
                    self._format_session_status(session.status),
                    self._blue(session.session_id),
                    session.target_name))
        else:
            self._output(self._red('No Sessions were found.'))
    ###############################################################################################
    #                               Target Methods                                                #
    ###############################################################################################
    @handle_exceptions
    def GetTarget(self, name, show_facts=False, hide_actions=False): #pylint: disable=invalid-name
        """
        Fetch information about a Target.

        Args:
            name: The name of the Target to search for.
            showfacts: Set True to display all facts
        """
        target = Target.get_target(name)

        if target:
            self._output(self._green('Target Found:\n'))
            self._output('\tname: {}'.format(target.name))
            self._output('\tstatus: {}'.format(self._format_session_status(target.status)))
            self._output('\tLast Seen: {}s ago'.format(time.time() - target.lastseen))
            self._output('\n\tHostname: {}'.format(
                self._yellow(target.facts.get('hostname', 'unknown hostname'))))
            ip_addrs = []
            for iface in target.facts.get('interfaces', []):
                addrs = iface.get('ip_addrs')
                if addrs:
                    for addr in addrs:
                        if addr != '127.0.0.1' and not addr.startswith('169.254'):
                            ip_addrs.append(addr)
            self._output('\tIP Addresses: {}'.format(self._yellow(', '.join(sorted(ip_addrs)))))
            if not hide_actions:
                actions = Target.list_target_actions(target.name)
                if actions:
                    self._output('\n\nActions:')
                for action in actions:
                    self._output('\naction_id: {}'.format(self._blue(action.action_id)))
                    self._output('action: {}'.format(self._yellow(action.action_string)))
                    self._output('status: {}'.format(self._format_action_status(action.status)))

            if show_facts:
                self._output('\nAll Facts:')
                self._output('\t{}'.format(self._format_facts(target.facts)))
        else:
            self._output(self._red('Target not found.'))


    @handle_exceptions
    def ListTargets(self): #pylint: disable=invalid-name
        """
        This lists all Targets that are currently tracked by the teamserver.

        Args:
            None
        """
        targets = Target.list_targets()
        if targets:
            for target in sorted(targets, key=lambda x: x.name):
                groups = Target.list_target_groups(target.name)
                self._output('[{}]\t{}\tgroups: {}'.format(
                    self._format_session_status(target.status),
                    self._blue(target.name),
                    self._green(', '.join(groups) if groups else 'None')
                ))
        else:
            self._output(self._red('No Targets were found.'))

    ###############################################################################################
    #                                 Log Methods                                                 #
    ###############################################################################################
    @handle_exceptions
    def ListLogs(self, application=None, since=None, include_archived=None):  #pylint: disable=invalid-name
        """
        This lists logs from the teamserver, and may be optionally filtered.

        Args:
            application(optional): The Application to filter for.
            since(optional): All logs returned will have a timestamp greater than this.
            include_archived(optional): Should archived logs be included in the search.
        """
        logs = Log.list_logs(application, since, include_archived)
        for log in logs:
            timestamp = datetime.fromtimestamp(log.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            self._output('[{}][{}]\t[{}]\t{}'.format(
                timestamp,
                self._blue(log.application),
                self._format_loglevel(log.level),
                log.message
            ))

if __name__ == '__main__':
    fire.Fire(ArsenalClient)
