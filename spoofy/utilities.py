from .settings import Settings
from sys import exc_info
from traceback import format_exception
import ctypes, os

def check_dependencies():
    """
    Check if required dependencies installed.

    Exit (2) if failed.
    """
    if (os.name == 'nt' and not os.path.exists('C:\\Windows\\SysWOW64\\Npcap')):
        print()
        print(f"{'':2}(e2) 'Npcap' is required to run on 'Windows'!")
        print(f"{'':2}Download via 'https://nmap.org/npcap/#download'")
        print()
        exit_(2)

def check_privilege():
    """
    Check if required privilege level for program to run is met.

    Exit (13) if failed.
    """
    if (os.name == 'nt'):
        privileged = (ctypes.windll.shell32.IsUserAnAdmin() != 0)
    else:
        privileged = (os.getuid() == 0)

    if (not privileged):
        print()
        print(f"{'':2}(e13) Need higher privilege to run!")
        print(f"{'':2}Please 'Run as administrator' on 'Windows'")
        print(f"{'':6}or 'sudo' on 'macOS' and 'Linux'")
        print()
        exit_(13)

def check_requirements():
    """
    Check requirements to run program.
    """
    check_dependencies()
    check_privilege()

def exit_(code):
    """
    Exit with given code and prevent auto-close when launched standalone.

    Parameter:
        code -- (int) exit code
    """
    if (code != 0):
        input("Press 'Enter' to continue... ")
    os._exit(code)

def input_(msg):
    """
    Return processed user input.
    """
    cmd = input(msg).strip().lower()
    for char in Settings.sanitize:
        cmd = cmd.replace(char, '')

    if (Settings.get['DEBUG']):
        print(f"{'':2}(d) repr(cmd): {repr(cmd)}")

    return cmd

def trace_exception(code=1):
    """
    Print exception error and information (file, line, method) and exit.

    Parameter:
        code -- (int/1) exit code
    """
    etype, value, tb = exc_info()
    info, error = format_exception(etype, value, tb)[-2:]

    print(f"{'':2}(e{code}) {error}")
    print(f"{'':2}{info.strip()}")
    print()
    print(f"{'':2}Unexpected error! Consider reporting via https://github.com/kgrv-me/spoofy/issues/new")
    print()
    exit_(code)