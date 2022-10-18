#!/usr/bin/env python
"""
This script looks at every XML file in the repo, and checks whether it
has a consistent filename.
"""

import os
import re

from tooling import GREEN, RED, RESET, get_file_paths_under


if __name__ == '__main__':
    errors = 0

    for path in get_file_paths_under(suffix=".xml"):
        filename = os.path.basename(path)

        if path.startswith("./Arabic/") and not re.match(r'^MS_Arabic_\d+\.xml$', filename):
            print(f'Unrecognised filename: {RED}{path}{RESET}')
            errors += 1

        if path.startswith("./Tibetan/") and not re.match(r'^MS_Tibetan_\d+\.xml$', filename):
            print(f'Unrecognised filename: {RED}{path}{RESET}')
            errors += 1

    if errors == 0:
        print(f"{GREEN}🎉 All paths checked, no errors!{RESET}")
    else:
        print(
            f"{RED}⚠️ All paths checked, {errors} error{'s' if errors > 0 else ''} found!{RESET}"
        )
        sys.exit(1)
