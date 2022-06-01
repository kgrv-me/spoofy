from pathlib import PurePath
from sysconfig import get_path

import json

class Settings():
    """
    Settings (configuration) for program.
    """
    __conf_file = str(PurePath(get_path('data'), 'settings.conf'))
    __get = {
        'DELAY': 0.3, # 0.3 is the minimum for CLI to work properly
        'SAFE_MODE': False,
        'WAIT_DURATION': 16 # 16 is the minimum for GoT:Legends splitting
    }
    __minimum_delay = 0.3

    commands = {
        'back': ['b', 'back', 'B', 'BACK', 'o', 'out', 'O', 'OUT'],
        'quit': ['e', 'exit', 'E', 'EXIT', 'q', 'quit', 'Q', 'QUIT'],
        'settings': ['s', 'setting', 'settings', 'S', 'SETTING', 'SETTINGS'],
        'kill': ['k', 'kill', 'K', 'KILL'],
        'unkill': ['u', 'unkill', 'un-kill', 'U', 'UNKILL', 'UN-KILL']
    }
    get = {}

    @classmethod
    def load_settings(cls):
        """
        Load settings from file if exists.
        """
        cls.get = cls.__get
        try:
            with open(cls.__conf_file, 'r') as cfg:
                cls.get = json.loads(cfg.read())
            if (cls.get['DELAY'] < cls.__minimum_delay):
                cls.get['DELAY'] = cls.__minimum_delay
        except:
            pass

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
        with open(cls.__conf_file, 'w') as cfg:
            cfg.write(json.dumps(cls.get))

    @classmethod
    def set_delay(cls, seconds):
        """
        Set 'DELAY' in float seconds.
        """
        if (not seconds.replace('.', '').isdecimal()):
            print("Invalid 'SECONDS' for 'DELAY'!")
        elif (float(seconds) < cls.__minimum_delay):
            print("'DELAY' needs to be greater than '0.3' seconds!")
        else:
            cls.get['DELAY'] = float(seconds)
            cls.save_settings()

    @classmethod
    def set_wait_duration(cls, seconds):
        """
        Set 'WAIT_DURATION' in float seconds.
        """
        cls.get['WAIT_DURATION'] = seconds
        cls.save_settings()
        print(f"'WAIT_DURATION' is now '{cls.get['WAIT_DURATION']}'")

    @classmethod
    def toggle_safe_mode(cls):
        """
        Toggle 'SAFE_MODE' ON/OFF for spoofing activity.
        """
        cls.get['SAFE_MODE'] = (not cls.get['SAFE_MODE'])
        cls.save_settings()
        print(f"'SAFE_MODE' is now '{cls.get['SAFE_MODE']}'")