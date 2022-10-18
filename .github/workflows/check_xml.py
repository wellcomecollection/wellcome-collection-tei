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

from tooling import RED, GREEN, RESET, BLUE, get_file_paths_under


def guess_line_label(path, text):
    """
    Given a file and some text, return a hint about where this text
    might appear.
    """
    lines = enumerate(list(open(path)), start=1)

    line_numbers = [lineno for lineno, line in lines if text in line]

    if len(line_numbers) == 0:
        return ""
    else:
        return (
            f"(try looking at {BLUE}{text}{RESET} on "
            + ", ".join(f"{BLUE}L{lineno}{RESET}" for lineno in line_numbers)
            + ")"
        )


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
        for author in root.findall(".//{http://www.tei-c.org/ns/1.0}author"):
            persname_nodes = author.findall("./{http://www.tei-c.org/ns/1.0}persName")

            if len(persname_nodes) <= 1:
                continue

            if not any(pn.attrib.get("type") == "original" for pn in persname_nodes):
                line_label = guess_line_label(path, text=persname_nodes[0].text.splitlines()[0])

                print("")
                print(os.path.relpath(path, start=repo_root))
                print(
                    f'\tFound <author> with multiple <persName> nodes but no type="original"'
                )
                if line_label:
                    print(f'\t{line_label}')
                errors += 1

        # We expect to see manuscript IDs in the form: 'MS $Language $Number',
        # e.g. 'MS Hebrew B1' or 'MS Arabic 247'.
        #
        # This looks for the manuscript ID in <idno type="msID">, and warns
        # if it's not as expected.
        #
        # We skip some special cases which are not currently handled by
        # this rule and need more work to fix.
        if "/Spanish/" in path or "/Indic/" in path or "/Greek/" in path:
            continue

        actual_manuscript_id = root.find(".//{http://www.tei-c.org/ns/1.0}idno[@type='msID']").text

        language = os.path.basename(os.path.dirname(path))

        # e.g. Hebrew_B_55.xml ~> B55, Tamil_49.xml ~> 49
        if "/Hebrew/" in path:
            ms_short_id = "".join(path.split(".")[0].rsplit("_")[-2:])
        else:
            ms_short_id = path.split("_")[-1].split(".")[0]

        expected_manuscript_id = f"MS {language} {ms_short_id}"

        if expected_manuscript_id != actual_manuscript_id:
            print("")
            print(os.path.relpath(path, start=repo_root))
            print(f'\tManuscript ID in <idno type="msID"> is malformed:')
            print(f'\t\tExpected: {GREEN}{expected_manuscript_id!r}{RESET}')
            print(f'\t\tActual:   {RED}{actual_manuscript_id!r}{RESET}')
            errors += 1

    print("")

    if errors == 0:
        print(f"{GREEN}🎉 All files checked, no errors!{RESET}")
    else:
        print(
            f"{RED}⚠️ All files checked, {errors} error{'s' if errors > 0 else ''} found!{RESET}"
        )
        sys.exit(1)
