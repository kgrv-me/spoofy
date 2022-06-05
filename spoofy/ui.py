from .network import Network
from .settings import Settings
from .signals import Signal
from .utilities import check_requirements, input_, trace_exception

class CLI():
    """
    UI class of CLI type to run program for user interaction.
    """
    #: Hold command for processing
    cmd = ''

    @classmethod
    def process_duration_input(cls, fnc, var):
        """
        Process user input for setting duration.

        Parameter:
            fnc -- (method) method to run if applicable
            var -- (string) configuration variable for Settings

        """
        cls.cmd = input_(f"Enter '{var}' interval (in seconds): ")
        if (cls.cmd.replace('.', '').isdecimal()):
            fnc(float(cls.cmd))
        elif (
            cls.cmd not in Settings.commands['back']
            and cls.cmd not in Settings.commands['quit']
            and cls.cmd != ''
        ):
            print(f"{'':2}(e22) Invalid interval for '{var}'!")
        elif (
            (cls.cmd not in Settings.commands['back']
            or cls.cmd != '')
            and cls.cmd not in Settings.commands['quit']
        ):
            cls.cmd = 'settings'

    @classmethod
    def process_host_selection(cls, safe_mode):
        """
        Process user input for host selection to spoof.

        Parameter:
            safe_mode -- (string) inline SAFE_MODE indicator
        """
        index = int(cls.cmd)
        host = Network.get_host_by_ip(str(Network.get['ip_list'][index]))
        while (
            cls.cmd not in Settings.commands['back']
            and cls.cmd not in Settings.commands['quit']
            and cls.cmd not in Settings.commands['stop']
        ):
            if (
                Settings.get['WAIT_DURATION'] == 0
                and cls.cmd not in Settings.commands['revive']
            ):
                Network.kill(host)
                print()
                cls.cmd = input_(f"Press 'Enter' to revive '{host['vendor']}' (b to go back):{safe_mode} ")
                if (cls.cmd == ''):
                    cls.cmd = 'revive'
            elif (
                Settings.get['WAIT_DURATION'] == 0
                and cls.cmd not in Settings.commands['kill']
            ):
                Network.revive(host)
                print()
                cls.cmd = input_(f"Press 'Enter' to spoofy '{host['vendor']}' (b to go back):{safe_mode} ")
                if (cls.cmd == ''):
                    cls.cmd = 'kill'
            else:
                Network.spoof(host)
                print()
                cls.cmd = input_(f"Press 'Enter' to spoof '{host['vendor']}' again (b to go back):{safe_mode} ")

    @classmethod
    def process_info_menu(cls):
        """
        Display software/system information.
        """
        sm = Settings.info['system']
        arch_info = '' if sm['ARCH'] in sm['PLATFORM'] else f" ({sm['ARCH']})"

        print()
        print(f"{'':2}Refer to embedded 'README.md' for documentation")
        print(f"{'':2}or visit https://github.com/kgrv-me/spoofy/blob/main/README.md")
        print()

        print(f"{'':2}Software")
        print(f"{'':4}Python {sm['PYTHON']}")
        if ('software' in Settings.info):
            sw = Settings.info['software']
            print(f"{'':4}Spoofy-{sw['OS']}-{sw['ARCH']} {sw['VERSION']}")
        print()

        print(f"{'':2}System")
        print(f"{'':4}{sm['PLATFORM']}{arch_info}")
        print()
        cls.cmd = input_("Press 'Enter' to go back... ")

    @classmethod
    def process_license_menu(cls):
        """
        Display information about license.
        """
        print()
        print(f"{'':2}GNU General Public License v3.0")
        print()
        print(f"{'':2}Refer to embedded 'LICENSE' for details")
        print(f"{'':2}or visit https://github.com/kgrv-me/spoofy/blob/main/LICENSE")
        print()
        print(f"{'':2}(Disclaimer) Use this software at your own risk!")
        print()
        cls.cmd = input_("Press 'Enter' to go back... ")

    @classmethod
    def process_main_menu(cls):
        """
        Process user input on main menu.

        List available hosts for selection.
        """
        # Menu
        print()
        for i, ip in enumerate(Network.get['ip_list']):
            h = Network.get_host_by_ip(str(ip))
            ip = str(ip).ljust(Network.get['max_ip_length'])
            print(f"{i:>3}) {ip}  |  {h['mac']}  |  {(h['vendor_tagged'])}")
        print()
        print(f"{'i':>3}) Information")
        print(f"{'l':>3}) GNU GPLv3 License")
        print(f"{'s':>3}) Settings Configuration")
        print()

        # Process commands
        auto_msg = ' temporary' if Settings.get['WAIT_DURATION'] != 0 else ''
        safe_mode = ' ~ SAFE_MODE ~' if Settings.get['SAFE_MODE'] else ''
        cls.cmd = input_(f"Select device to{auto_msg} disconnect (q to quit):{safe_mode} ")
        if (cls.cmd in Settings.commands['info']):
            cls.process_info_menu()
        elif (cls.cmd in Settings.commands['license']):
            cls.process_license_menu()
        elif (cls.cmd in Settings.commands['settings']):
            cls.process_settings_menu()
        elif (cls.cmd.isdecimal() and int(cls.cmd) < len(Network.get['hosts'])):
            cls.process_host_selection(safe_mode)
        elif (cls.cmd in Settings.commands['specials']):
            cls.process_special_cmd()
        elif (
            cls.cmd not in Settings.commands['quit']
            and cls.cmd != ''
        ):
            print(f"{'':2}(e22) Invalid selection!")

    @classmethod
    def process_settings_menu(cls):
        """
        Process user input on settings menu.

        List available settings for selection.
        """
        # Menu
        print()
        print(f"{'n':>3}) Network scan for local hosts")
        print(f"{'r':>3}) Reset settings configuration")
        print(f"{'s':>3}) Toggle 'SAFE_MODE' for spoofing (Current: {Settings.get['SAFE_MODE']})")
        print(f"{'t':>3}) Set 'TIMEOUT' for ARP requests (Current: {Settings.get['TIMEOUT']})")
        print(f"{'w':>3}) Set 'WAIT_DURATION' to enable auto-revive (Current: {Settings.get['WAIT_DURATION']})")
        print()

        # Process commands
        cls.cmd = input_("Select setting to configure (b to go back): ")
        if (cls.cmd == 'n'):
            Network.initialize()
        elif (cls.cmd == 'r'):
            Settings.reset_settings()
        elif (cls.cmd == 's'):
            Settings.toggle_safe_mode()
        elif (cls.cmd == 't'):
            cls.process_duration_input(Settings.set_timeout, 'TIMEOUT')
        elif (cls.cmd == 'w'):
            cls.process_duration_input(Settings.set_wait_duration, 'WAIT_DURATION')
        elif (cls.cmd in Settings.commands['specials']):
            cls.process_special_cmd()
        elif (
            cls.cmd not in Settings.commands['back']
            and cls.cmd not in Settings.commands['quit']
            and cls.cmd != ''
        ):
            print(f"{'':2}(e22) Invalid setting selection!")

        # Return if empty, quit, back, or network scan command
        if (
            cls.cmd in Settings.commands['back']
            or cls.cmd in Settings.commands['quit']
            or cls.cmd == ''
            or cls.cmd == 'n'
            or cls.cmd == '!!scan'
        ):
            return

        # Stay in settings menu
        cls.process_settings_menu()

    @classmethod
    def process_special_cmd(cls):
        """
        Process user input for special commands.
        """
        if (cls.cmd == '!debug'):
            Settings.toggle_debug_mode()
        elif (cls.cmd == '!!delay'):
            cls.process_duration_input(Settings.set_delay, 'DELAY')
        elif (cls.cmd == '!!reset'):
            Settings.reset_settings()
        elif (cls.cmd == '!safe-mode'):
            Settings.toggle_safe_mode()
        elif (cls.cmd == '!!scan'):
            Network.initialize()
        elif (cls.cmd == '!!settings'):
            Settings.print_debug(debug=True)
        elif (cls.cmd == '!!timeout'):
            cls.process_duration_input(Settings.set_timeout, 'TIMEOUT')
        elif (cls.cmd == '!!wait'):
            cls.process_duration_input(Settings.set_wait_duration, 'WAIT_DURATION')

    @classmethod
    def run(cls):
        """
        Main method to run this component.
        """
        try:
            # Initialize signal handling
            Signal.handlers()

            # Check requirements to run
            check_requirements()

            print()
            print("Welcome to 'Spoofy'!")
            print("A cross-platform CLI Python package for ARP spoofing!")
            print()

            Settings.initialize()
            Network.initialize()
            while (cls.cmd not in Settings.commands['quit']):
                cls.process_main_menu()
        except EOFError:
            cls.terminate()
        except:
            cls.terminate()
            trace_exception()
        else:
            Network.cleanup()
            print()

    @classmethod
    def terminate(cls, space=True):
        """
        Invoke Signal.terminate() if interrupted.

        Parameter:
            space -- (bool/True) pad 2 extra newlines before the message
        """
        Signal.terminate(space=space)