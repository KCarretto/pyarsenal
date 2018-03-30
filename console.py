"""
This module wraps the Arsenal cli.py to provide an interactive shell.
"""
from cli import ArsenalClient

import fire
import os
import platform
import shlex
import subprocess
import sys
import threading

# Import readline
HAS_READLINE = True
try:
    import readline
except ImportError:
    print("Warning: readline not installed. Limited shell capability.")
    HAS_READLINE = False

# Remap input, for python 2/3 compatibility
try:
    input = raw_input
except NameError:
    pass

# Globals
PROMPT = "Arsenal >> "
HIST_FILE = ".arsenal_history"
ALIAS = {}

# Run Fire in separate thread to prevent exiting
class FireThread(threading.Thread):
    def __init__(self, cmd):
        self._cmd = cmd
        threading.Thread.__init__(self)

    def run(self):
        fire.Fire(ArsenalClient, '{}'.format(self._cmd))

# Tab completion for our console
class SimpleCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

def banner():
    print(
    """
    Welcome to Arsenal v 1.0

                                                          \|/
                                                         .-*-
                                                        / /|\
                                                       _L_
                                                     ,"   ".
                                                 (\ /  O O  \ /)
                                                  \|    _    |/
                                                    \  (_)  /
                                                    _/.___,\_
                                                   (_/     \_)

    Use the help command to view function docstrings (i.e. 'help ListTargets' )

    You can alias keywords by issuing the command 'alias <keyword> <value>'.
        This will replace all instances of keyword with value in the issued command.
        Remove this alias with the command 'unalias <keyword>'

    You can issue local system commands by issuing the command 'shell <cmd>'
    """
    )

def parse_command(cmd):
    # Handle Aliases
    for k,v in ALIAS.items():
        cmd = cmd.replace(k, v)
    return cmd

def clear():
    p = subprocess.Popen( "cls" if platform.system() == "Windows" else "echo -e \\\\033c", shell=True)
    p.wait()

def exit():
    print("\nThanks for using Arsenal")
    sys.exit(0)

def main():

    # Configure readline
    if HAS_READLINE:
        if os.path.exists(HIST_FILE):
            readline.read_history_file(HIST_FILE)
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')
        completer = SimpleCompleter(filter(lambda x: not x.startswith('_'), dir(ArsenalClient)))
        readline.set_completer(completer.complete)

    # Loop for input
    cleared = False

    # Display the banner
    banner()

    while True:
        if cleared:
            cleared = False
            continue

        try:
            cmd = input(PROMPT)
            args = shlex.split(cmd)
            if cmd.lower() == 'exit' or cmd.lower() == 'quit':
                exit()
            elif cmd.lower() == 'clear' or cmd.lower() == 'cls':
                clear()
                cleared = True
            elif len(args) > 0 and args[0].lower() == 'alias':
                if len(args) == 1:
                    print('')
                    for k,v in ALIAS.items():
                        print('\t{}\t->\t{}'.format(k,v))
                    print('')
                    continue
                elif len(args) < 3:
                    print("Usage: alias <keyword> <value>")
                    continue
                else:
                    ALIAS[args[1]] = args[2]
            elif len(args) > 0 and args[0].lower() == 'unalias':
                if len(args) > 1 and args[1] in ALIAS.keys():
                    del ALIAS[args[1]]
                else:
                    print("Encountered error")
                continue
            elif len(args) > 0 and args[0].lower() == 'shell':
                print("")
                p = subprocess.Popen(' '.join(args[1:]), shell=True)
                p.wait()
                print("")
                sys.stdout.flush()
                sys.stderr.flush()
                continue
            else:
                cmd = parse_command(cmd)

                t1 = FireThread(cmd)
                t1.start()
                t1.join()
                if HAS_READLINE:
                    readline.write_history_file(HIST_FILE)
        except EOFError as e:
            exit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()