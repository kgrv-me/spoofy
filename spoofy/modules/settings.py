from pathlib import PurePath
from sysconfig import get_path

import json

class Settings():
    """
    Settings (configuration) for program.
    """
    __conf_file = str(PurePath(get_path('data'), 'settings.conf'))
    __conf_file_bak = None
    __get = {
        'DEBUG': False,
        'DELAY': 0.3, # 0.3 is the minimum for CLI to work properly
        'SAFE_MODE': False,
        'WAIT_DURATION': 0 # 16 is the minimum for GoT:Legends splitting (for me)
    }
    __minimum_delay = 0.3

    commands = {
        'back': ['b', 'back', 'B', 'BACK', 'o', 'out', 'O', 'OUT'],
        'quit': ['e', 'exit', 'E', 'EXIT', 'q', 'quit', 'Q', 'QUIT'],
        'license': ['l', 'license', 'L', 'LICENSE'],
        'settings': ['s', 'setting', 'settings', 'S', 'SETTING', 'SETTINGS'],
        'kill': ['k', 'kill', 'K', 'KILL'],
        'revive': ['r', 'revive', 'R', 'REVIVE', 'u', 'unkill', 'un-kill', 'U', 'UNKILL', 'UN-KILL']
    }
    get = {}

    @classmethod
    def __load_settings(cls, path):
        """
        Load settings from file if exists.
        """
        with open(path, 'r') as cfg:
            cls.get = json.loads(cfg.read())
        if (cls.get['DELAY'] < cls.__minimum_delay):
            cls.get['DELAY'] = cls.__minimum_delay

    @classmethod
    def __save_settings(cls, path):
        """
        Save settings to file.
        """
        with open(path, 'w') as cfg:
            cfg.write(json.dumps(cls.get))

    @classmethod
    def load_settings(cls):
        """
        Load settings from file if exists.
        """
        cls.get = cls.__get

        # Configure backup path for persistent settings
        loader_resource = __loader__.get_resource_reader(__name__)
        cls.__conf_file_bak = None if not loader_resource else str(PurePath(__loader__.get_resource_reader(__name__).path, 'settings.conf'))

        try:
            cls.__load_settings(cls.__conf_file)
        except:
            try:
                cls.__load_settings(cls.__conf_file_bak)
            except:
                pass

        if (cls.get['DEBUG']):
            print(f"{'':2}(d) Settings:")
            print(f"{'':4}{cls.get}")
            print(f"{'':2}(d) Settings.__conf_file:")
            print(f"{'':4}{cls.__conf_file}")
            print(f"{'':2}(d) Settings.__conf_file_bak:")
            print(f"{'':4}{cls.__conf_file_bak}")

    @classmethod
    def reset_settings(cls):
        """
        Reset settings to default configuration and save.
        """
        cls.get = cls.__get
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
        """
        if (not seconds.replace('.', '').isdecimal()):
            print(f"{'':2}Invalid 'SECONDS' for 'DELAY'!")
        elif (float(seconds) < cls.__minimum_delay):
            print(f"{'':2}'DELAY' needs to be greater than '0.3' seconds!")
        else:
            cls.get['DELAY'] = float(seconds)
            cls.save_settings()

    @classmethod
    def set_wait_duration(cls, seconds):
        """
        Set 'WAIT_DURATION' in float seconds.
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