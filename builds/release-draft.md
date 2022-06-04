Refer to [README.md](https://github.com/kgrv-me/spoofy/blob/main/README.md) for detailed information


## REQUIREMENT
### Host Network
- `Spoofy` needs host network access to work correctly
- Ensure compatible network settings in VMs before use

### Super User Privilege (Administrative Rights)
- `Run as administrator` on `Windows`
- `sudo` on `macOS` and `Linux`

### Windows
- `Npcap` (Download https://nmap.org/npcap/#download)


## USAGE
- [CLI](https://github.com/kgrv-me/spoofy#cli)
  - [About Information](https://github.com/kgrv-me/spoofy#about-information)
  - [Settings](https://github.com/kgrv-me/spoofy#settings)
  - [Safe Mode](https://github.com/kgrv-me/spoofy#safe-mode)
  - [Spoofing (Default)](https://github.com/kgrv-me/spoofy#spoofing-default)
  - [Spoofing (Automatically)](https://github.com/kgrv-me/spoofy#spoofing-automatically)
  - [Interruption](https://github.com/kgrv-me/spoofy#interruption)

### Run as Standalone
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

#### Cannot be opened on macOS
Executable needs to be allowed through `Gatekeeper` on `macOS` first with
```
- Hold 'Control ^'
- Right click on 'Spoofy-macOS-ARM64'
- Select 'Open' from context menu
- Click 'Open' button on prompt
```


## CHANGELOG
```

```