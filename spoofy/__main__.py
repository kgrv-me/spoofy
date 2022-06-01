#!/usr/bin/env python3

from spoofy.modules.ui import CLI
from spoofy.modules.utilities import check_requirements

if __name__ == '__main__':
    try:
        # Check required privilege to run
        check_requirements()

        # Run UI
        CLI.run()
    except KeyboardInterrupt:
        CLI.terminate()
    except EOFError:
        CLI.terminate()
    except Exception as err:
        if (err):
            print(f"(e1) {err}")
        CLI.terminate()