A cross-platform CLI Python package for spoofing! (*Created for Ghost of Tsushima: Legends*)

[REQUIREMENT](#requirement) - [OS/ARCH](#osarch) - [USAGE](#usage) ( [Run as Python Module](#run-as-python-module) | [Run as Standalone](#run-as-standalone) | [CLI](#cli) ) - [CHANGELOG](#changelog)


## REQUIREMENT
### Python Module (Not Required for Standalone)
- `Python3` (Download https://www.python.org/downloads/)

### Super User Privilege (Administrator Right)
- `sudo` on `macOS` and `Linux`
- `Run as administrator` on `Windows`

### Windows
- `Npcap` (Download https://nmap.org/npcap/#download)


## OS/ARCH
*Standalone Executable*
| OS/ARCH          | Description |
| :--------------: | ----------- |
| `Linux/x86_64`   | 64-bit x86 architecture for Linux operating systems |
| `macOS/ARM64`    | 64-bit ARM architecture for macOS operating systems |
| `macOS/x86_64`   | 64-bit x86 architecture for macOS operating systems |
| `Windows/x86_64` | 64-bit x86 architecture for Windows operating systems |


## USAGE
### Run as Python Module
Clone `git` repository
```
git clone https://github.com/kgrv-me/spoofy.git
```
Install dependencies
```
pip3 install --requirement requirements.txt
```
or utilize built-in virtual environment for isolation
```
python3 -m venv DIR
source DIR/bin/activate
```
Run as Python module inside the repository
```
python3 -m spoofy
```

### Run as Standalone
**NOTE:** Ensure to only download from trusted sources!

There is `run.sh` for `macOS` and `Linux` to help run `sudo`

*Right click and 'Run as administrator' on executable for `Windows`*
```
~ Spoofy
  - LICENSE
  - README.md
  - run.sh
  - Spoofy-macOS-ARM64
```
or run the executable via terminal
```
sudo ./Spoofy-macOS-ARM64
```


### CLI
*Requires higher privilege to run!*
```
~ ./Spoofy-macOS-ARM64

(e13) Need higher privilege to run!
Please 'Run as administrator' on 'Windows'
    or 'sudo' on 'macOS' and 'Linux'

Press 'Enter' to continue...
```
It will scan network for local hosts automatically
```
~ sudo ./Spoofy-macOS-ARM64

Welcome to 'Spoofy'!
Scanning network for hosts...

0) 192.168.1.1  |  aa:bb:cc:dd:ee:ff  |  Intel
1) 192.168.1.2  |  ff:ee:dd:cc:bb:aa  |  Apple
2) 192.168.1.3  |  11:22:33:44:55:66  |  CloudNet (PS)
s) Settings (NETWORK_SCAN, RESET_SETTINGS, SAFE_MODE, WAIT_DURATION)

Select device to temporary disconnect (q to quit): _
```

#### Settings
Enter `s` as input for configurable settings
```
n) Network scan for local hosts
r) Reset settings configuration
s) Toggle 'SAFE_MODE' for spoofing (Current: False)
w) Set 'WAIT_DURATION' between KILL and UN-KILL (Current: 16)
   Set 'WAIT_DURATION' to 0 to disable auto UN-KILL

Select setting to configure (b to go back): _
```
`Spoofy` saves edited settings configuration to `settings.conf` for persistency
```
~ Spoofy
  ..
  - settings.conf
  - Spoofy-macOS-ARM64
```
`Spoofy` will **NOT** send network packets in `SAFE_MODE`
```
'SAFE_MODE' is now 'True'

0) 192.168.1.1  |  aa:bb:cc:dd:ee:ff  |  Intel
1) 192.168.1.2  |  ff:ee:dd:cc:bb:aa  |  Apple
2) 192.168.1.3  |  11:22:33:44:55:66  |  CloudNet (PS)
s) Settings (NETWORK_SCAN, RESET_SETTINGS, SAFE_MODE, WAIT_DURATION)

~ SAFE_MODE: ON ~
Select device to temporary disconnect (q to quit): _
```

#### Spoofing (Automatically)
Once selected, `Spoofy` will poison ARP cache for 'WAIT_DURATION' (Default: 16s)
```
~ SAFE_MODE: ON ~
Select device to temporary disconnect (q to quit): 2
'11:22:33:44:55:66 - CloudNet' is killed
'11:22:33:44:55:66 - CloudNet' is un-killed

Press 'Enter' to spoof 'CloudNet' again (b to go back): _
```
*Pressing 'Enter' will spoof the same target again!*

#### Spoofing (Manually)
or manual toggle by setting 'WAIT_DURATION' to 0
```
n) Network scan for local hosts
r) Reset settings configuration
s) Toggle 'SAFE_MODE' for spoofing (Current: True)
w) Set 'WAIT_DURATION' between KILL and UN-KILL (Current: 16)
   Set 'WAIT_DURATION' to 0 to disable auto UN-KILL

~ SAFE_MODE: ON ~
Select setting to configure (b to go back): w
Enter duration (in seconds): 0
'WAIT_DURATION' is now '0.0'
```
Press 'Enter' to toggle between KILL and UN-KILL
```
~ SAFE_MODE: ON ~
Select device to temporary disconnect (q to quit): 2
'11:22:33:44:55:66 - CloudNet' is killed

Press 'Enter' to un-kill 'CloudNet' (b to go back): 
'11:22:33:44:55:66 - CloudNet' is un-killed

Press 'Enter' to kill 'CloudNet' (b to go back): _
```


## CHANGELOG
### 2022-06-01
#### v0.3-RC
```
Added
- manual toggle mode by setting 'WAIT_DURATION' to 0
- persistent settings saving to 'settings.conf'
- settings configuration reset

Changed
- 'Network.kill()' and 'Network.unkill()' argument to support manual toggle
- 'patch.sh' to 'patch.py' for GitHub Actions workflow 'invalid cross-device' error

Improved
- cleanup coverage to ensure proper ARP cache reset before termination
- exceptions handling for better stability and UX
- UI, UX elements in CLI

Updated
- 'build.sh' to support both local and GitHub Actions runner
- command handling to not error out on quit commands
- GitHub Actions workflow to build 'macOS-x86_64', 'Linux-x86_64', 'Windows-x86_64'
- 'pyoxidizer.bzl' for size optimization
```

### 2022-05-31
#### v0.2.4-ALPHA
```
Added
- 'patch.sh' to address '__file__' conflict with 'pyoxidizer'

Changed
- '0.0.0.0' to '1.1.1.1' for gateway fetching

Fixed
- OS dependent path separator for GitHub Actions workflow

Removed
- 'ipaddress' from requirements (already built-in)
- 'psutil' package

Updated
- 'network.py'
    - get netmask via system call
    - to better utilize 'scapy.conf.iface' reducing redundancy
- 'pyoxidizer.bzl' to compile standalone executable without '.so' from 'psutil'
```

### 2022-05-30
#### v0.2.3-ALPHA
```
Added
- 'build.sh' script
- 'pyoxidizer' for standalone

Removed
- 'pyinstaller' from workflow
```

### 2022-05-29
#### v0.2.2-ALPHA
```
Fixed
- 'pyinstaller' standalone compiling

Updated
- 'psutil' from '5.9.0' to '5.9.1'
```

### 2022-05-21
#### v0.2.1-ALPHA
```
Added
- 'pyinstaller' for standalone

Fixed
- inter-package import error
```

### 2022-05-20
#### v0.2-ALPHA
```
Added
- Configurable settings
- GitHub Actions workflow
- Requirements check

Updated
- 'spoofy.py' module into proper 'spoofy' package
```

### 2022-05-19
#### v0.1-ALPHA
```
Added
- 'ipaddress', 'manuf', 'psutil', 'scapy' packages
- 'spoofy.py' Python Module
```