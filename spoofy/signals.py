from .ui import CLI
from .utilities import exit_
from signal import *
import os

class Signal():
    """
    Signal class to handle system signals.
    """
    @classmethod
    def handlers(cls):
        """
        Initialize signal handlers to allow graceful termination.
        """
        # Abort signal from abort(3)
        signal(SIGABRT, cls.terminate)
        # Keyboard interruption
        signal(SIGINT, cls.terminate)
        # Terminate signal
        signal(SIGTERM, cls.terminate)
        if (os.name != 'nt'):
            # Stop signal
            signal(SIGTSTP, cls.terminate)

    @classmethod
    def terminate(cls, signum, frame):
        """
        Handle catched signal.
        """
        print()
        print()
        print(f"Terminating due to SIGNAL:{signum}")
        CLI.terminate(space=False)
        exit_(0)