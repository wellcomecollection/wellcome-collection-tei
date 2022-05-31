#!/usr/bin/env python

import os
import subprocess
from xml.etree import ElementTree as ET


RED   = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"


def get_file_paths_under(root=".", *, suffix=""):
    """Generates the paths to every file under ``root``."""
    if not os.path.isdir(root):
        raise ValueError(f"Cannot find files under non-existent directory: {root!r}")

    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if os.path.isfile(os.path.join(dirpath, f)) and f.lower().endswith(suffix):
                yield os.path.join(dirpath, f)


if __name__ == '__main__':
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel', ]).strip().decode('ascii')

    errors = 0

    for path in get_file_paths_under(root, suffix='.xml'):
        try:
            ET.parse(path)
        except ET.ParseError as err:
            if errors > 0:
                print("")

            print(os.path.relpath(path, start=root))
            print(f"\t{err}")
            errors += 1

    print("")

    if errors == 0:
        print(f"{GREEN}🎉 All files checked, no errors!{RESET}")
    else:
        print(f"{RED}⚠️ All files checked, {errors}{'s' if errors > 0 else ''} errors found!{RESET}")
