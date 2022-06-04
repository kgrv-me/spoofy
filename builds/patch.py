#!/usr/bin/env python3

from pathlib import PurePath
from subprocess import check_output
from yaml import CLoader, load
import sys

def exec_patch(patch):
    """
    Apply patch from 'patch.yaml'.
    """
    lib_path = check_output("pip3 show scapy | grep Location | cut -d ' ' -f2", shell=True).decode().rstrip().replace('\\', '\\\\')

    for p in sorted(patch):
        print(f"{'':2}Patching '{p}'...")
        for f in sorted(patch[p]):
            fp = str(PurePath(lib_path, p, f))
            print(f"{'':4}File '{fp}'")
            with open(fp, 'r') as of:
                content = of.read()

            if ('replace' in patch[p][f]):
                for find in patch[p][f]['replace']:
                    replace = patch[p][f]['replace'][find]
                    print(f"{'':6}Replace '{find}' with '{replace}'")
                    content = content.replace(find, replace)
            content = content.split('\n')

            if ('delete' in patch[p][f]):
                for ds in sorted(patch[p][f]['delete']):
                    de = patch[p][f]['delete'][ds]
                    print(f"{'':6}Delete line '{ds}' to '{de}'")
                    del content[ds-1:de]

            if ('insert' in patch[p][f]):
                for il in sorted(patch[p][f]['insert']):
                    text = patch[p][f]['insert'][il]
                    if ('{' in text):
                        si = text.find('{')
                        ei = text.find('}')
                        space = int(text[si+1:ei])
                        text = f"{''.join(' ' for _ in range(space))}{text[ei+1:]}"
                    print(f"{'':6}Insert line '{il}' with '{text}'")
                    content.insert(il-1, text)
            content = '\n'.join(line for line in content)

            # Overwrite target with patch
            with open(fp, 'w') as of:
                of.write(content)

def get_patch():
    """
    Get patch from 'patch.yaml'.
    """
    patch_path = __file__.replace('.py', '.yaml')
    print(f"{'':2}Load patch from '{patch_path}'")
    with open(patch_path, 'r') as f:
        patch = load(f, Loader=CLoader)
    return patch

def refresh_packages(packages):
    """
    Reinstall Python packages for patching.
    """
    print(f"{'':2}Refreshing '{packages}'...")
    check_output(f"pip3 uninstall -y {packages} && pip3 install {packages}", shell=True)

def run():
    """
    Main method to run this script.
    """
    patch = get_patch()
    if ('refresh-packages' in sys.argv):
        refresh_packages(' '.join(patch.keys()))
    exec_patch(patch)

if __name__ == '__main__':
    run()