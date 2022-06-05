from .network import Network
from .utilities import exit_
from signal import *
import os

class Signal():
    """
    Signal class to handle system signals.
    """
    @classmethod
    def __terminate(cls, signum, frame):
        """
        Handle catched signal.
        """
        print()
        print()
        print(f"Terminating due to SIGNAL:{signum}")
        cls.terminate(space=False)
        exit_(0)

    @classmethod
    def handlers(cls):
        """
        Initialize signal handlers to allow graceful termination.
        """
        # Abort signal from abort(3)
        signal(SIGABRT, cls.__terminate)
        # Keyboard interruption
        signal(SIGINT, cls.__terminate)
        # Terminate signal
        signal(SIGTERM, cls.__terminate)
        if (os.name != 'nt'):
            # Stop signal
            signal(SIGTSTP, cls.__terminate)

    @classmethod
    def terminate(cls, space=True):
        """
        Invoke in case of interruption to properly terminate.

        Parameter:
            space -- (bool/True) pad 2 extra newlines before the message
        """
        if (Network.get_killed() > 0):
            if (space):
                print()
                print()
            print("Initiate cleanup process... DO NOT interrupt!")
        Network.cleanup()
        print()