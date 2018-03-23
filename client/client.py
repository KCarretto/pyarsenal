"""
This module includes a class that contains all API functions,
and may be called from the command line.
"""
import colorama
import fire

from .action import Action
from .session import Session


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
        # TODO: Include response

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
    def GetSession(self, session_id): #pylint: disable=invalid-name
        """
        This method fetches an Session from the teamserver.

        Args:
            session_id: The identifier of the Session to fetch.
        """
        session = Session.get_session(session_id)

        self._output(self._green('Session Found:\n'))
        self._output('\tsession_id: {}'.format(self._blue(session.session_id)))
        self._output('\tstatus: {}'.format(self._format_session_status(session.status)))

    def ListSessions(self): #pylint: disable=invalid-name
        """
        This lists all Sessions that are currently tracked by the teamserver.

        Args:
            None
        """
        sessions = Session.list_sessions()
        if sessions:
            for session in sessions:
                self._output('[{}][{}]\t (Target: {})'.format(
                    self._format_session_status(session.status),
                    self._blue(session.session_id),
                    session.target_name))
        else:
            self._output(self._red('No Sessions were found.'))

if __name__ == '__main__':
    fire.Fire(ArsenalClient)
