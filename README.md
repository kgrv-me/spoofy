A cross-platform CLI Python package for spoofing! *Inspired by [`elmoCut`](https://github.com/elmoiv/elmocut)*

[REQUIREMENT](#requirement) - [OS/ARCH](#osarch) - [USAGE](#usage) ( [Run as Python Module](#run-as-python-module) | [Run as Standalone](#run-as-standalone) | [CLI](#cli) ) - [CHANGELOG](#changelog)


## REQUIREMENT
### Python Module (Not Required for Standalone)
- `Python3` (Download https://www.python.org/downloads/)

### Super User Privilege (Administrator Right)
- `Run as administrator` on `Windows`
- `sudo` on `macOS` and `Linux`

### Windows
- `Npcap` (Download https://nmap.org/npcap/#download)


## OS/ARCH
*Standalone Executable*
| OS/ARCH          | Description |
| :--------------: | ----------- |
| `Linux/x86_64`   | 64-bit `x86` architecture for `Linux` operating systems |
| `macOS/ARM64`    | 64-bit `ARM` architecture for `macOS` operating systems |
| `macOS/x86_64`   | 64-bit `x86` architecture for `macOS` operating systems |
| `Windows/x86_64` | 64-bit `x86` architecture for `Windows` operating systems |


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
or utilize built-in virtual environment before installing
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

  l) GNU GPLv3 License
  s) Settings Configuration

Select device to disconnect (q to quit): _
```

#### Settings
Enter `s` as input for configurable settings
```
  n) Network scan for local hosts
  r) Reset settings configuration
  s) Toggle 'SAFE_MODE' for spoofing (Current: True)
  w) Set 'WAIT_DURATION' to enable auto-revive (Current: 0)

Select setting to configure (b to go back): _
```
`Spoofy` saves edited settings configuration to `settings.conf` for persistency
```
~ Spoofy
  ..
  - settings.conf
  - Spoofy-macOS-ARM64
```

#### Safe Mode
`Spoofy` will **NOT** send network packets in `SAFE_MODE`
```
  'SAFE_MODE' is now 'True'

  0) 192.168.1.1  |  aa:bb:cc:dd:ee:ff  |  Intel
  1) 192.168.1.2  |  ff:ee:dd:cc:bb:aa  |  Apple
  2) 192.168.1.3  |  11:22:33:44:55:66  |  CloudNet (PS)

  l) GNU GPLv3 License
  s) Settings Configuration

Select device to disconnect (q to quit): ~ SAFE_MODE ~ _
```

#### Spoofing (Default)
Once selected, `Spoofy` will poison ARP cache until stopped

*Press 'Enter' to toggle between KILL and REVIVE*
```
Select device to disconnect (q to quit): 2
  '11:22:33:44:55:66 - CloudNet' is killed

Press 'Enter' to revive 'CloudNet' (b to go back): 
  '11:22:33:44:55:66 - CloudNet' is revived

Press 'Enter' to spoofy 'CloudNet' (b to go back): _
```

#### Spoofing (Automatically)
or auto-revive by setting 'WAIT_DURATION'
```
  n) Network scan for local hosts
  r) Reset settings configuration
  s) Toggle 'SAFE_MODE' for spoofing (Current: True)
  w) Set 'WAIT_DURATION' to enable auto-revive (Current: 0)

Select setting to configure (b to go back): w
Enter duration (in seconds): 16
  'WAIT_DURATION' is now '16.0'
```
*Pressing 'Enter' will spoof the same target again!*
```
Select device to temporary disconnect (q to quit): 2
  '11:22:33:44:55:66 - CloudNet' is killed
  '11:22:33:44:55:66 - CloudNet' is revived

Press 'Enter' to spoof 'CloudNet' again (b to go back): _
```

#### Interruption
`Spoofy` resets killed hosts before termination
```
Press 'Enter' to revive 'CloudNet' (b to go back): q
Resetting spoofed hosts...
  '11:22:33:44:55:66 - CloudNet' is revived
```
`CTRL-C`
```
Press 'Enter' to revive 'CloudNet' (b to go back): ^C

Terminating due to SIGNAL:2
Initiate cleanup process... DO NOT interrupt!
Resetting spoofed hosts...
  '11:22:33:44:55:66 - CloudNet' is revived
```
`CTRL-D`
```
Press 'Enter' to revive 'CloudNet' (b to go back): ^D

Initiate cleanup process... DO NOT interrupt!
Resetting spoofed hosts...
  '11:22:33:44:55:66 - CloudNet' is revived
```
`CTRL-Z`
```
Press 'Enter' to revive 'CloudNet' (b to go back): ^Z

Terminating due to SIGNAL:18
Initiate cleanup process... DO NOT interrupt!
Resetting spoofed hosts...
  '11:22:33:44:55:66 - CloudNet' is revived
```

## CHANGELOG
### 2022-06-02
#### v0.4-rc
```
Added
- adaptive spacing for hosts IP addresses list
- debug mode
- license menu
- non-blocking exit if code '0'
- signal handling for graceful termination
- sorting hosts by IP in 'Network.get_hosts()' for consistent listing

Changed
- default spoofing mode to manual
- 'Network.unkill()' to 'Network.revive()'
- 'Network.kill()', 'Network.revive()', 'Network.spoof()' argument to support sorted hosts
- 'SAFE_MODE' indicator to be inline input prompt

Improved
- input command formatting for more flexibility
- persistent settings with backup location and better check for stability

Updated
- display messages formats for better UI, UX
- 'Settings' commands
```

### 2022-06-01
#### v0.3-rc
```
Added
- manual toggle mode by setting 'WAIT_DURATION' to 0
- persistent settings with 'settings.conf'
- settings configuration reset

Changed
- 'Network.kill()' and 'Network.unkill()' argument to support manual toggle
- 'patch.sh' to 'patch.py' for GitHub Actions workflow 'invalid cross-device' error

Improved
- cleanup coverage to ensure proper ARP cache reset before termination
- exceptions handling for better stability and UX
- UI, UX elements in 'ui.CLI'

Updated
- 'build.sh' to support both local and GitHub Actions runner
- command handling to not error out on quit commands
- GitHub Actions workflow to build 'macOS-x86_64', 'Linux-x86_64', 'Windows-x86_64'
- 'pyoxidizer.bzl' for size optimization
```

### 2022-05-31
#### v0.2.4-alpha
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
#### v0.2.3-alpha
```
Added
- 'build.sh' script
- 'pyoxidizer' for standalone

Removed
- 'pyinstaller' from workflow
```

### 2022-05-29
#### v0.2.2-alpha
```
Fixed
- 'pyinstaller' standalone compiling

Updated
- 'psutil' from '5.9.0' to '5.9.1'
```

### 2022-05-21
#### v0.2.1-alpha
```
Added
- 'pyinstaller' for standalone

Fixed
- inter-package import error
```

### 2022-05-20
#### v0.2-alpha
```
Added
- Configurable settings
- GitHub Actions workflow
- Requirements check

Updated
- 'spoofy.py' module into proper 'spoofy' package
```

### 2022-05-19
#### v0.1-alpha
```
Added
- 'ipaddress', 'manuf', 'psutil', 'scapy' packages
- 'spoofy.py' Python Module
```