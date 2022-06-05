"""
A cross-platform CLI Python package for ARP spoofing!

https://github.com/kgrv-me/spoofy
"""

# Collect all modules for ease of import
from .network import Network
from .settings import Settings
from .signals import Signal
from .ui import CLI
from .utilities import *

# pdoc3 overwrite
__pdoc__ = {
    '__main__': True
}