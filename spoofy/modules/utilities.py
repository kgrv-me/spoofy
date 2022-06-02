from threading import Thread
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
        exit(2)

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
        exit(13)

def check_requirements():
    """
    Check requirements to run program.
    """
    check_dependencies()
    check_privilege()

def exit(code):
    """
    Exit with given code and prevent auto-close when launching standalone.
    """
    if (code != 0):
        input("Press 'Enter' to continue...")
    os._exit(code)

def threaded(fn):
    """
    Run method in thread to avoid blocking.
    """
    def run(*k, **kw):
        t = Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t
    return run