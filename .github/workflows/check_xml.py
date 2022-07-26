#!/usr/bin/env python
"""
This script looks at every XML file in the repo, and checks whether it
can be parsed as valid XML.  It also does some basic linting.

This doesn't mean it can be parsed and used in the catalogue pipeline
by the Digital Engagement team, but it's a useful first pass.
"""

import os
import subprocess
import sys
from xml.etree import ElementTree as ET


RED = "\033[1;31m"
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


if __name__ == "__main__":
    repo_root = (
        subprocess.check_output(
            [
                "git",
                "rev-parse",
                "--show-toplevel",
            ]
        )
        .strip()
        .decode("ascii")
    )

    errors = 0

    for path in sorted(get_file_paths_under(repo_root, suffix=".xml")):

        # Exclude a couple of paths that aren't actual TEI files
        if os.path.relpath(path, start=repo_root).startswith(("Templates/", "docs/")):
            continue

        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as err:
            print("")
            print(os.path.relpath(path, start=repo_root))
            print(f"\tUnable to parse XML: {err}")
            errors += 1
            continue

        # The transformer expects to see author names in the form:
        #
        #       <author key="person_88345215">
        #           <persName xml:lang="eng" type="standard">Badr-addin Muhammad b. Bahram b. Muhammad al-Qalanisi as-Samarqandi</persName>
        #           <persName xml:lang="ar" type="original">بدر الدين محمد بن بهرام بن محمد القلانسي السمرقندي</persName>
        #       </author>
        #
        # Notice that one is labelled `type="original"`; if this is missing,
        # we don't know what contributor to display on the page.
        for author in root.findall('.//{http://www.tei-c.org/ns/1.0}author'):
            persname_nodes = author.findall('./{http://www.tei-c.org/ns/1.0}persName')

            if len(persname_nodes) <= 1:
                continue

            if not any(pn.attrib.get('type') == 'original' for pn in persname_nodes):
                print("")
                print(os.path.relpath(path, start=repo_root))
                print(f"\tFound <author> with multiple <persName> nodes but no type=\"original\"")
                errors += 1
                break

    print("")

    if errors == 0:
        print(f"{GREEN}🎉 All files checked, no errors!{RESET}")
    else:
        print(
            f"{RED}⚠️ All files checked, {errors} error{'s' if errors > 0 else ''} found!{RESET}"
        )
        sys.exit(1)
