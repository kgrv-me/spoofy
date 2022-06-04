A cross-platform CLI Python package for spoofing! *Inspired by [`elmoCut`](https://github.com/elmoiv/elmocut)*

[REQUIREMENT](#requirement) - [OS/ARCH](#osarch) - [USAGE](#usage) ( [Run as Standalone](#run-as-standalone) | [Run as Python Module](#run-as-python-module) | [CLI](#cli) ) - [CHANGELOG](#changelog)


## REQUIREMENT
### Host Network
- `Spoofy` needs host network access to work correctly
- Ensure compatible network settings in VMs before use
  - `Parallels`, `VirtualBox`, `VMware`

### Python Module (Not Required for Standalone)
- `Python3` (Download https://www.python.org/downloads/)

### Super User Privilege (Administrative Rights)
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
### Run as Standalone
**NOTE:** Ensure to only download from trusted sources!

**Official Release:** https://github.com/kgrv-me/spoofy/releases/latest

- *Double click* `run.sh` to run on `macOS` and `Linux` (`.sh` needs to open with `Terminal`)
- *Right click* on `Spoofy-Windows-x86_64.exe` and select `Run as administrator` on `Windows`
```
[ macOS ]                   [ Linux ]                   [ Windows ]
~ Spoofy                    ~ Spoofy                    ~ Spoofy
  - LICENSE                   - LICENSE                   ~ lib
  - README.md                 - README.md                 - LICENSE
  > run.sh                    > run.sh                    - python3.dll
  - Spoofy-macOS-ARM64        - Spoofy-Linux-x86_64       - python39.dll
                                                          - README.md
                                                          > Spoofy-Windows-x86_64.exe
                                                          - vcruntime140.dll
                                                          - vcruntime140_1.dll
```

or run the executable via terminal on `macOS` and `Linux`
```
sudo ./Spoofy-macOS-ARM64
```

#### Cannot be opened on macOS
Executable needs to be allowed through `Gatekeeper` on `macOS` first with
```
- Hold 'Control ^'
- Right click on 'Spoofy-macOS-ARM64'
- Select 'Open' from context menu
- Click 'Open' button on prompt
```

or through system preferences
```
- Open 'System Preferences'
- Select 'Security & Privacy'
- Select 'General' tab
- There should be '"Spoofy-macOS-ARM64" was blocked ..' message
- Click 'Open Anyway' button
- Click 'Open' button on prompt
```
`Spoofy` is now allowed to run!

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
sudo python3 -m spoofy
```
*`Terminal` needs to be `Run as administrator` on `Windows`*

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

  i) Information
  l) GNU GPLv3 License
  s) Settings Configuration

Select device to disconnect (q to quit): _
```

#### About Information
Enter `i` in main menu to display relevant information
```
  Refer to embedded 'README.md' for documentation
  or visit https://github.com/kgrv-me/spoofy/blob/main/README.md

  Repository
    https://github.com/kgrv-me/spoofy

  Software
    Python 3.10.4
    Spoofy-macOS-ARM64 v1.0-rc

  System
    macOS-12.4-arm64-arm-64bit

Press 'Enter' to go back... _
```

#### Settings
Enter `s` as input for configurable settings
```
  n) Network scan for local hosts
  r) Reset settings configuration
  s) Toggle 'SAFE_MODE' for spoofing (Current: False)
  w) Set 'WAIT_DURATION' to enable auto-revive (Current: 0)

Select setting to configure (b to go back): _
```

`Spoofy` saves edited settings configuration to `settings.json` for persistency
```
~ Spoofy
  ..
  - settings.json
  - Spoofy-macOS-ARM64
```

#### Safe Mode
`Spoofy` will **NOT** send network packets in `SAFE_MODE`
```
  'SAFE_MODE' is now 'True'

  0) 192.168.1.1  |  aa:bb:cc:dd:ee:ff  |  Intel
  1) 192.168.1.2  |  ff:ee:dd:cc:bb:aa  |  Apple
  2) 192.168.1.3  |  11:22:33:44:55:66  |  CloudNet (PS)

  i) Information
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
### 2022-06-05
#### v1.0
```
Added
- 'CLI.input_()' with input sanitation
- GitHub templates for issue/feature
- 'INFO' for standalone during build process
- information menu
- 'patch.yaml' patch file
- 'release-draft.md' for release template
- 'requirements-build.txt' for Python dependencies in build process
- 'Settings'
    - 'get_info()' to load embedded 'INFO' with measurement against spoofing
    - 'initialize()' to call instead of 'load_settings()'
    - to fetch system and Python information

Changed
- build structure to directory 'builds'

Updated
- 'build.sh' to support 'PyOxidizer' configure and 'INFO'
- 'build.yaml' for new build structure and capabilities
- 'CLI' to utilize 'cls.input_()'
- 'patch.py' to utilize 'patch.yaml'
- 'Settings'
    - '__load_settings()' to be ~20x faster
    - to support 'CLI.input_()' and 'INFO'
```

### 2022-06-03
#### v0.5-rc
```
Added
- API documentation with 'pdoc3'
- exception trace in 'utilities.trace_exception()'
- 'main()' in '__main__.py' for importing
- 'signals.py' module

Changed
- package structure to flat modules
- 'settings.conf' to 'settings.json'
- 'utilities.exit()' to 'utilities.exit_()' to avoid confusion with built-in

Fixed
- 'Network.get_netmask()' issue on 'Linux'

Removed
- 'modules' sub-module

Updated
- '__main__.py' to utilize 'signals.Signal'
- package docstring and restructure for API documentation
- 'run.sh' to run 'sudo' in its place
```

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
- 'run.sh' to be more compatible with older systems
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