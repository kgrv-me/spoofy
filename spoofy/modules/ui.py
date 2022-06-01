from time import sleep

from .network import Network
from .settings import Settings

class CLI():
    """
    UI class of CLI type to run program for user interaction.
    """
    cmd = ''

    @classmethod
    def process_main_menu(cls):
        """
        Process user input on main menu.
        List available hosts for selection.
        """
        # Menu
        print()
        for i, h in enumerate(Network.get['hosts']):
            print(f"{i}) {h['ip']:13} |  {h['mac']}  |  {(h['vendor_tagged'])}")
        print("s) Settings (NETWORK_SCAN, RESET_SETTINGS, SAFE_MODE, WAIT_DURATION)")
        print()

        # Process command
        if (Settings.get['SAFE_MODE']):
            print("~ SAFE_MODE: ON ~")
        auto_msg = ' temporary' if Settings.get['WAIT_DURATION'] != 0 else ''
        cls.cmd = input(f"Select device to{auto_msg} disconnect (q to quit): ")
        if (cls.cmd in Settings.commands['settings']):
            cls.process_settings_menu()
        elif (cls.cmd.isdecimal() and int(cls.cmd) < len(Network.get['hosts'])):
            index = int(cls.cmd)
            while (
                cls.cmd not in Settings.commands['back']
                and cls.cmd not in Settings.commands['quit']
            ):
                if (
                    Settings.get['WAIT_DURATION'] == 0
                    and cls.cmd not in Settings.commands['unkill']
                ):
                    Network.kill(index)
                    print()
                    cls.cmd = input(f"Press 'Enter' to un-kill '{Network.get['hosts'][index]['vendor']}' (b to go back): ")
                    if (cls.cmd == ''):
                        cls.cmd = 'unkill'
                elif (
                    Settings.get['WAIT_DURATION'] == 0
                    and cls.cmd not in Settings.commands['kill']
                ):
                    Network.unkill(index)
                    sleep(Settings.get['DELAY'])
                    print()
                    cls.cmd = input(f"Press 'Enter' to kill '{Network.get['hosts'][index]['vendor']}' (b to go back): ")
                    if (cls.cmd == ''):
                        cls.cmd = 'kill'
                else:
                    Network.spoof(index)
                    sleep(Settings.get['DELAY'])
                    print()
                    cls.cmd = input(f"Press 'Enter' to spoof '{Network.get['hosts'][index]['vendor']}' again (b to go back): ")
        elif (cls.cmd not in Settings.commands['quit']):
            print("(e22) Invalid host selection!")

    @classmethod
    def process_settings_menu(cls):
        """
        Process user input on settings menu.
        List available settings for selection.
        """
        # Menu
        print()
        print("n) Network scan for local hosts")
        print("r) Reset settings configuration")
        print(f"s) Toggle 'SAFE_MODE' for spoofing (Current: {Settings.get['SAFE_MODE']})")
        print(f"w) Set 'WAIT_DURATION' between KILL and UN-KILL (Current: {Settings.get['WAIT_DURATION']})")
        print(f"{' ':2} Set 'WAIT_DURATION' to 0 to disable auto UN-KILL")
        print()

        # Process command
        if (Settings.get['SAFE_MODE']):
            print("~ SAFE_MODE: ON ~")
        cls.cmd = input("Select setting to configure (b to go back): ")
        if (cls.cmd == 'n'):
            Network.initialize()
        elif (cls.cmd == 'r'):
            Settings.reset_settings()
        elif (cls.cmd == 's'):
            Settings.toggle_safe_mode()
        elif (cls.cmd == 'w'):
            cls.cmd = input("Enter duration (in seconds): ")
            if (cls.cmd.replace('.', '').isdecimal()):
                Settings.set_wait_duration(float(cls.cmd))
            else:
                print("(e22) Invalid duration for 'WAIT_DURATION'!")
        elif (
            cls.cmd not in Settings.commands['back']
            and cls.cmd not in Settings.commands['quit']
        ):
            print("(e22) Invalid setting selection!")

    @classmethod
    def run(cls):
        """
        Main method to run this component.
        """
        print()
        print("Welcome to 'Spoofy'!")
        Settings.load_settings()
        Network.initialize()

        while (cls.cmd not in Settings.commands['quit']):
            cls.process_main_menu()
        Network.cleanup()
        print()

    @classmethod
    def terminate(cls):
        """
        Invoke in case of interruption to properly terminate.
        """
        print()
        print()
        if (Network.get_killed() > 0):
            print("Initiate cleanup process... DO NOT interrupt!")
        Network.cleanup()
        print()