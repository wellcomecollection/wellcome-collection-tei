#!/usr/bin/env python
"""
This script looks at every XML file in the repo, and checks whether it
can be parsed as valid XML.

This doesn't mean it can be parsed and used in the catalogue pipeline
by the Digital Engagement team, but it's a useful first pass.
"""

import os
import subprocess
import sys
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

        # We don't parse the contents of the Templates directory as XML;
        # it's meant for humans to read, not computers
        if path.startswith('Templates/'):
            continue

        try:
            ET.parse(path)
        except ET.ParseError as err:
            print("")
            print(os.path.relpath(path, start=root))
            print(f"\t{err}")
            errors += 1

    print("")

    if errors == 0:
        print(f"{GREEN}🎉 All files checked, no errors!{RESET}")
    else:
        print(f"{RED}⚠️ All files checked, {errors} error{'s' if errors > 0 else ''} found!{RESET}")
        sys.exit(1)
