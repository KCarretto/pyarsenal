"""
The console is a wrapper around the cli.py client, and provides an interactive terminal.
"""
from __future__ import unicode_literals

import sys
import threading
import time

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
    pass

class ShellExit(Exception):
    """
    Raised when the user exits a shell.
    """
    pass

class ArsenalCompleter(Completer): # pylint: disable-all
    """
    A completer specific to the Arsenal API.
    """
    _api_methods = []
    _built_ins = []
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

        self._built_ins = ['help', 'interact', 'exit', 'reset']

        self.target_names = autocomplete.get('target_names', [])
        self.group_names = autocomplete.get('group_names', [])
        self.role_names = autocomplete.get('role_names', [])
        self.agent_names = autocomplete.get('agent_names', [])
        self.user_names = autocomplete.get('user_names', [])

        self.auto_completers = {
            'help': [
                WordCompleter(self._api_methods)
            ],
            'interact': [
                WordCompleter(self.target_names)
            ],
            'reset': [],
            'exit': [],
            'GetTarget': [
                WordCompleter(self.target_names)
            ],
            'DeleteGroup': [
                WordCompleter(self.group_names)
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
            'AddGroupRule': [
                WordCompleter(self.group_names)
            ],
            'RemoveGroupRule': [
                WordCompleter(self.group_names)
            ],
            'AddGroupMember': [
                WordCompleter(self.group_names),
                WordCompleter(self.target_names),
            ],
            'RemoveGroupMember': [
                WordCompleter(self.group_names),
                WordCompleter(self.target_names),
            ],
            'BlacklistGroupMember': [
                WordCompleter(self.group_names),
                WordCompleter(self.target_names)
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
            ],
            'RenameTarget': [
                WordCompleter(self.target_names)
            ]
        }

        self.api_completer = WordCompleter(list(set(self._api_methods+self._built_ins)), True)

    def get_completions(self, document, complete_event):
        """
        A function for determining auto-complete results.
        """
        words = document.text.split(' ')

        if words and (words[0] in self._api_methods or words[0] in self._built_ins):
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

class Executor(threading.Thread):
    """
    Run CreateAction in a separate thread, waiting for the action to complete.
    """
    def __init__(self, client, target_name, cmd):
        self.target_name = target_name
        self.client = client
        self.cmd = cmd
        threading.Thread.__init__(self)

    @handle_exceptions
    def run(self):
        action_id = self.client.create_action(
            self.target_name, 'exec {}'.format(self.cmd), None, None, True)

        resp = None
        start = time.time()

        # Poll, waiting for action to complete
        while not resp:
            try:
                action = self.client.get_action(action_id)
                if hasattr(action, 'response') and action.response:
                    resp = action.response
                    break
                if time.time() > start + 30:
                    print('Action has timed out.')
                    break
            except KeyboardInterrupt:
                break

            time.sleep(1)

        print(resp.get('stdout', ''), file=sys.stdout)
        print(resp.get('stderr', ''), file=sys.stderr)


def shell(client, target_name):
    """
    Join an interactive shell for a target. Still uses the normal beacons, but automatically
    adds the --quick flag to create action, and polls for output.
    """
    history = InMemoryHistory()

    print('\nEntering into arsenal shell. \n \
        Please note commands may take a while to execute, depending on session intervals. \n\n')

    executor = None

    while True:
        try:
            text = prompt(
                'Arsenal [{}] # '.format(target_name),
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
            )

            if text.lower() == 'exit' or text.lower() == 'quit':
                break

            if text.strip() == '':
                continue

            background = False
            if text.lower().startswith('&'):
                text = text[1:]
                background = True

            executor = Executor(client, target_name, text)
            executor.start()
            if background:
                print("Backgrounded job. Output will display once completed.")
            else:
                executor.join()

        except EOFError:
            break
        except KeyboardInterrupt:
            continue
        except Exception:
            break

    if executor and isinstance(executor, Executor):
        executor.join()

    raise ShellExit()

def exit_arsenal():
    """
    Exit the console
    """
    print("\nThanks for using Arsenal")
    sys.exit(0)

def parse_command(client, text):
    """
    Parse the input from the console.
    """
    cmd = text.lower()

    if cmd == 'exit':
        exit_arsenal()
    if cmd == 'reset':
        raise Reset()
    if cmd.startswith('interact'):
        tokens = cmd.split(' ')
        if len(tokens) < 2:
            print('usage: interact <target name>')
            raise ShellExit()
        shell(client, cmd.split(' ')[1])
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
    try:
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
    except:
        pass

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
                text = parse_command(cli.client, text)
                firethread = FireThread(text, cli)
                firethread.start()
                firethread.join()
                print('')
        except Reset:
            cli.client.context = cli.client.get_current_context()
            methods = cli.client.context.allowed_api_calls
            autocomplete = build_autocomplete(cli.client)
        except ShellExit:
            pass
        except EOFError:
            exit_arsenal()
        except KeyboardInterrupt:
            exit_arsenal()
        except Exception as exception: # pylint: disable=broad-except
            print(exception)

if __name__ == '__main__':
    main()
