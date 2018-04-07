"""
The console is a wrapper around the cli.py client, and provides an interactive terminal.
"""
from __future__ import unicode_literals

import sys
import threading

import fire

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from cli import CLI
from pyclient import API_KEY_FILE
from pyclient.exceptions import handle_exceptions, PermissionDenied

class Reset(Exception):
    """
    Raised when the user wishes to reinitialize the terminal.
    """

class ArsenalCompleter(Completer): # pylint: disable-all
    """
    A completer specific to the Arsenal API.
    """
    _api_methods = {}
    target_names = []
    group_names = []
    role_names = []
    agent_names = []
    user_names = []
    def __init__(self, methods, autocomplete):
        """
        Constructor for the completer, used to gather API information.
        """
        self._api_methods = methods
        if '*' in self._api_methods:
            self._api_methods = list(filter(lambda x: not x.startswith('_'), dir(CLI)))

        self.target_names = autocomplete.get('target_names', [])
        self.group_names = autocomplete.get('group_names', [])
        self.role_names = autocomplete.get('role_names', [])
        self.agent_names = autocomplete.get('agent_names', [])
        self.user_names = autocomplete.get('user_names', [])

        self.auto_completers = {
            'GetTarget': [
                WordCompleter(self.target_names)
            ],
            'GetGroup': [
                WordCompleter(self.group_names)
            ],
            'CreateAction': [
                WordCompleter(self.target_names)
            ],
            'CreateGroupAction': [
                WordCompleter(self.group_names)
            ],
            'AddRoleMember': [
                WordCompleter(self.role_names),
                WordCompleter(self.user_names),
            ],
            'RemoveRoleMember': [
                WordCompleter(self.role_names),
                WordCompleter(self.user_names),
            ],
            'GetUser': [
                WordCompleter(self.user_names)
            ],
            'GetRole': [
                WordCompleter(self.role_names)
            ]
        }

        self.api_completer = WordCompleter(self._api_methods, True)

    def get_completions(self, document, complete_event):
        """
        A function for determining auto-complete results.
        """
        words = document.text.split(' ')

        if words and words[0] in self._api_methods:
            completers = self.auto_completers.get(words[0])
            if completers:
                try:
                    completer = completers[len(words)-2]
                    if completer:
                        yield from (Completion(
                            completion.text,
                            completion.start_position,
                            display=completion.display)
                                    for completion
                                    in completer.get_completions(document, complete_event))
                except IndexError:
                    pass
        else:
            yield from (Completion(
                completion.text,
                completion.start_position,
                display=completion.display)
                        for completion
                        in self.api_completer.get_completions(document, complete_event))

class FireThread(threading.Thread):
    """
    Creates a separate thread and calls the google fire library on the Arsenal client.
    """
    def __init__(self, cmd, cli=None):
        self._cmd = cmd
        self.cli = cli
        if not self.cli:
            self.cli = CLI(api_key_file=API_KEY_FILE)
        threading.Thread.__init__(self)

    @handle_exceptions
    def run(self):
        fire.Fire(self.cli, '{}'.format(self._cmd))

def exit_arsenal():
    """
    Exit the console
    """
    print("\nThanks for using Arsenal")
    sys.exit(0)

def parse_command(text):
    """
    Parse the input from the console.
    """
    cmd = text.lower()

    if cmd == 'exit':
        exit_arsenal()
    if cmd == 'reset':
        raise Reset()
    return text

def build_autocomplete(client):
    """
    Return a dictionary for autocompletion.
    """
    resp = {
        'target_names': [],
        'group_names': [],
        'role_names': [],
        'agent_versions': [],
        'user_names': [],
    }
    def safe_discover(method, **kwargs):
        """
        Attempt to fetch autocomplete information, but return [] if permission is denied.
        """
        try:
            if kwargs.keys():
                return method(**kwargs)
            return method()
        except PermissionDenied:
            return []
        except Exception as exception:
            print(type(exception))
            print(exception)
    resp['target_names'] = [
        target.name for target in safe_discover(client.list_targets, include_status=False)]
    resp['group_names'] = [
        group.name for group in safe_discover(client.list_groups)]
    resp['role_names'] = [
        role.name for role in safe_discover(client.list_roles)]
    resp['agent_names'] = [
        agent.name for agent in safe_discover(client.list_agents)]
    resp['user_names'] = [
        user.username for user in safe_discover(client.list_users)]

    return resp

def main():
    """
    The main entry point of the program.
    """
    cli = CLI(api_key_file=API_KEY_FILE)
    history = InMemoryHistory()

    # Build Autocomplete
    methods = cli.client.context.allowed_api_calls
    autocomplete = build_autocomplete(cli.client)

    while True:
        try:
            text = prompt(
                'Arsenal >> ',
                completer=ArsenalCompleter(methods, autocomplete),
                history=history,
                auto_suggest=AutoSuggestFromHistory()
            )
            if text:
                text = parse_command(text)
                firethread = FireThread(text, cli)
                firethread.start()
                firethread.join()
                print('')
        except Reset:
            cli.client.context = cli.client.get_current_context()
            methods = cli.client.context.allowed_api_calls
            autocomplete = build_autocomplete(cli.client)
        except EOFError:
            exit_arsenal()
        except KeyboardInterrupt:
            exit_arsenal()
        except Exception as exception: # pylint: disable=broad-except
            print(exception)

if __name__ == '__main__':
    main()
