from pathlib import PurePath
from platform import machine, platform, python_version
from sysconfig import get_path
import contextlib
import importlib.resources
import json

class Settings():
    """
    Settings configuration for program.
    """
    __conf_file = str(PurePath(get_path('data'), 'settings.json'))
    __conf_file_bak = None
    __get = {}
    __minimum_delay = 0.1
    __minimum_timeout = 0.3 # 0.3 is the minimum for active host to respond

    #: Dictionary of valid commands lists
    commands = {
        # Global commands
        'back': ['b', 'back', 'o', 'out'],
        'quit': ['e', 'exit', 'q', 'quit'],

        # Menu selection
        'info': ['i', 'info', 'information'],
        'license': ['l', 'license'],
        'settings': ['s', 'setting', 'settings'],

        # Spoof commands
        'kill': ['k', 'kill'],
        'revive': ['r', 'revive', 'u', 'unkill', 'un-kill'],
        'stop': ['s', 'stop'],

        # Special commands
        'specials': ['!debug', '!!delay', '!!reset', '!safe-mode', '!!scan', '!!settings', '!!timeout', '!!wait']
    }
    #: Dictionary data structure
    get = {
        'DEBUG': False,
        'DELAY': 0.1,
        'SAFE_MODE': False,
        'TIMEOUT': 0.5,
        'WAIT_DURATION': 0
        # 16 is the minimum for GoT:Legends splitting (for me)
    }
    #: Dictionary software information
    info = {
        'system': {'ARCH': machine(), 'PLATFORM': platform(), 'PYTHON': python_version()}
    }
    #: List of characters to sanitize for input
    sanitize = [
        # Arrows (^, v, >, <)
        '\x1b[a', '\x1b[b', '\x1b[c', '\x1b[d',
        # Command + Arrows
        '\x05', '\x01',
        # Option + Arrows
        '\x1b[1;3a', '\x1b[1;3b', '\x1bf', '\x1bb',
        # Fn + Arrows
        '\x1b[5~', '\x1b[6~', '\x1b[f', '\x1b[h'
    ]

    @classmethod
    def __load_settings(cls, path):
        """
        Load settings from file if exists.

        Parameter:
            path -- (string) target path
        """
        with open(path, 'r') as cfg:
            cls.get = json.load(cfg)
        if (cls.get['DELAY'] < cls.__minimum_delay):
            cls.get['DELAY'] = cls.__minimum_delay
        if (cls.get['TIMEOUT'] < cls.__minimum_timeout):
            cls.get['TIMEOUT'] = cls.__minimum_timeout

    @classmethod
    def __save_settings(cls, path):
        """
        Save settings to file.

        Parameter:
            path -- (string) target path
        """
        with open(path, 'w') as cfg:
            cfg.write(json.dumps(cls.get))

    @classmethod
    def initialize(cls):
        """
        Get info and load settings if applicable.
        """
        cls.load_settings()
        cls.load_info()
        cls.print_debug()

    @classmethod
    def load_info(cls):
        """
        Load info information from INFO file.
        """
        try:
            path = importlib.resources.path(__package__, 'INFO')
            if (cls.get['DEBUG']):
                print(f"{'':2}(d) INFO Type")
                print(f"{'':4}{type(path)}")
            if (isinstance(path, contextlib._GeneratorContextManager)):
                with importlib.resources.open_binary(__package__, 'INFO') as info:
                    cls.info['software'] = json.load(info)
        except:
            pass

    @classmethod
    def load_settings(cls):
        """
        Load settings from file if exists.
        """
        cls.__get = dict(cls.get)

        # Configure backup path for persistent settings
        loader_resource = __loader__.get_resource_reader(__name__)
        cls.__conf_file_bak = None if not loader_resource else str(PurePath(__loader__.get_resource_reader(__name__).path, 'settings.json'))

        try:
            cls.__load_settings(cls.__conf_file)
        except:
            try:
                cls.__load_settings(cls.__conf_file_bak)
            except:
                pass

    @classmethod
    def print_debug(cls, debug=False):
        """
        Print debug information if in debug mode.

        Parameter:
            debug -- (bool/False) overwrite DEBUG setting
        """
        if (debug or cls.get['DEBUG']):
            print(f"{'':2}(d) Settings.get")
            print(f"{'':4}{cls.get}")
            print(f"{'':2}(d) Settings.info")
            print(f"{'':4}{cls.info}")
            print(f"{'':2}(d) Settings.__conf_file")
            print(f"{'':4}{cls.__conf_file}")
            print(f"{'':2}(d) Settings.__conf_file_bak")
            print(f"{'':4}{cls.__conf_file_bak}")

    @classmethod
    def reset_settings(cls):
        """
        Reset settings to default configuration and save.
        """
        cls.get = dict(cls.__get)
        cls.save_settings()

    @classmethod
    def save_settings(cls):
        """
        Save settings to file.
        """
        try:
            cls.__save_settings(cls.__conf_file)
        except:
            try:
                cls.__save_settings(cls.__conf_file_bak)
            except:
                print(f"{'':2}(w) Persistent Settings Unavailable")

    @classmethod
    def set_delay(cls, seconds):
        """
        Set 'DELAY' in float seconds.

        Parameter:
            seconds -- (float) amount of seconds
        """
        if (seconds < cls.__minimum_delay):
            print(f"{'':2}(w) 'DELAY' needs to be at least '{cls.__minimum_delay}' seconds!")
            seconds = cls.__minimum_delay

        cls.get['DELAY'] = seconds
        print(f"{'':2}'DELAY' is now '{cls.get['DELAY']}'")
        cls.save_settings()

    @classmethod
    def set_timeout(cls, seconds):
        """
        Set 'TIMEOUT' in float seconds.

        Parameter:
            seconds -- (float) amount of seconds
        """
        if (seconds < cls.__minimum_timeout):
            print(f"{'':2}(w) 'TIMEOUT' needs to be at least '{cls.__minimum_timeout}' seconds!")
            seconds = cls.__minimum_timeout

        cls.get['TIMEOUT'] = seconds
        print(f"{'':2}'TIMEOUT' is now '{cls.get['TIMEOUT']}'")
        cls.save_settings()

    @classmethod
    def set_wait_duration(cls, seconds):
        """
        Set 'WAIT_DURATION' in float seconds.

        Parameter:
            seconds -- (float) amount of seconds
        """
        cls.get['WAIT_DURATION'] = seconds
        print(f"{'':2}'WAIT_DURATION' is now '{cls.get['WAIT_DURATION']}'")
        cls.save_settings()

    @classmethod
    def toggle_debug_mode(cls):
        """
        Toggle 'DEBUG' ON/OFF for developer.
        """
        cls.get['DEBUG'] = (not cls.get['DEBUG'])
        print(f"{'':2}'DEBUG' is now '{cls.get['DEBUG']}'")
        cls.save_settings()

    @classmethod
    def toggle_safe_mode(cls):
        """
        Toggle 'SAFE_MODE' ON/OFF for spoofing activity.
        """
        cls.get['SAFE_MODE'] = (not cls.get['SAFE_MODE'])
        print(f"{'':2}'SAFE_MODE' is now '{cls.get['SAFE_MODE']}'")
        cls.save_settings()