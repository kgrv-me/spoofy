#!/usr/bin/env python3

from signal import *
from spoofy.modules.ui import CLI
from spoofy.modules.utilities import check_requirements, exit

import os

def signal_handlers():
    """
    Initialize signal handlers to allow graceful termination.
    """
    # Abort signal from abort(3)
    signal(SIGABRT, signal_termination)
    # Keyboard interruption
    signal(SIGINT, signal_termination)
    # Terminate signal
    signal(SIGTERM, signal_termination)
    if (os.name != 'nt'):
        # Stop signal
        signal(SIGTSTP, signal_termination)

def signal_termination(signum, frame):
    """
    Handle catched signal.
    """
    print()
    print()
    print(f"Terminating due to SIGNAL:{signum}")
    CLI.terminate(space=False)
    exit(0)

if __name__ == '__main__':
    try:
        # Initialize signal handling
        signal_handlers()

        # Check required privilege to run
        check_requirements()

        # Run UI
        CLI.run()
    except EOFError:
        CLI.terminate()
    except Exception as err:
        CLI.terminate()
        if (err):
            print(f"{'':2}(e1) {err}")
            print(f"{'':2}Unexpected error! Consider reporting via https://github.com/kgrv-me/spoofy/issues/new")
            print()
            exit(1)