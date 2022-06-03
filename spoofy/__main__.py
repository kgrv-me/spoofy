#!/usr/bin/env python3

from spoofy.signals import Signal
from spoofy.ui import CLI
from spoofy.utilities import check_requirements, trace_exception

def main():
    """
    Run package with CLI as main.
    """
    try:
        # Initialize signal handling
        Signal.handlers()

        # Check requirements to run
        check_requirements()

        # Run UI
        CLI.run()
    except EOFError:
        CLI.terminate()
    except:
        CLI.terminate()
        trace_exception()

if __name__ == '__main__':
    main()