#!/usr/bin/env python
"""
This script looks at every XML file in the repo, and checks whether it
can be parsed as valid XML.  It also does some basic linting.

This doesn't mean it can be parsed and used in the catalogue pipeline
by the Digital Engagement team, but it's a useful first pass.
"""

import collections
import os
import subprocess
import sys
import textwrap
from xml.etree import ElementTree as ET

from validation_rules import (
    check_for_author_names_with_no_original,
    check_for_malformed_manuscript_ids,
)


RED = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BLUE = "\033[1;34m"


def get_file_paths_under(root=".", *, suffix=""):
    """Generates the paths to every file under ``root``."""
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if os.path.isfile(os.path.join(dirpath, f)) and f.lower().endswith(suffix):
                yield os.path.join(dirpath, f)


def get_repo_root():
    return (
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


if __name__ == "__main__":
    repo_root = get_repo_root()

    errors = collections.defaultdict(list)

    for path in sorted(get_file_paths_under(repo_root, suffix=".xml")):

        # Exclude a couple of paths that aren't actual TEI files
        if os.path.relpath(path, start=repo_root).startswith(
            ("Templates/", "docs/", "minimum-viable-records/")
        ):
            continue

        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as err:
            errors[path].append(f"Unable to parse XML: {err}")
            continue

        validation_rules = [
            check_for_author_names_with_no_original,
            check_for_malformed_manuscript_ids,
        ]

        for run_rule in validation_rules:
            for e in run_rule(root, path):
                errors[path].append(e)

    if not errors:
        print(f"{GREEN}🎉 All files checked, no errors!{RESET}")
    else:
        for path, per_file_errors in sorted(errors.items()):
            print("")
            print(f"{BLUE}{os.path.relpath(path, repo_root)}{RESET}")
            for e in per_file_errors:
                print(textwrap.indent(e, prefix="\t"))

        total_errors = sum(len(v) for v in errors.values())

        print(
            f"{RED}⚠️ All files checked, {total_errors} error{'s' if total_errors > 0 else ''} found!{RESET}"
        )
        sys.exit(1)
