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

from collections import defaultdict
from xml.etree import ElementTree as ET


RED   = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BLUE  = "\033[1;34m"
XMLNS = {"": "http://www.tei-c.org/ns/1.0"}

def get_file_paths_under(root=".", *, suffix=""):
    """Generates the paths to every file under ``root``."""
    if not os.path.isdir(root):
        raise ValueError(f"Cannot find files under non-existent directory: {root!r}")

    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if os.path.isfile(os.path.join(dirpath, f)) and f.lower().endswith(suffix):
                yield os.path.join(dirpath, f)


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


def check_author_names(relpath, root, fullpath):
    # The transformer expects to see author names in the form:
    #
    #       <author key="person_88345215">
    #           <persName xml:lang="eng" type="standard">Badr-addin Muhammad b. Bahram b. Muhammad al-Qalanisi as-Samarqandi</persName>
    #           <persName xml:lang="ar" type="original">بدر الدين محمد بن بهرام بن محمد القلانسي السمرقندي</persName>
    #       </author>
    #
    # Notice that one is labelled `type="original"`; if this is missing,
    # we don't know what contributor to display on the page.
    errors = 0
    for author in root.findall(".//author", namespaces=XMLNS):
        persname_nodes = author.findall("./persName", namespaces=XMLNS)

        if len(persname_nodes) <= 1:
            continue

        if not any(pn.attrib.get("type") == "original" for pn in persname_nodes):
            line_label = guess_line_label(fullpath, text=persname_nodes[0].text.splitlines()[0])

            print("")
            print(relpath)
            print(
                f'\tFound <author> with multiple <persName> nodes but no type="original"'
            )
            if line_label:
                print(f'\t{line_label}')
            errors += 1
    return errors


def check_manuscript_id(relpath, root):
    # We expect to see manuscript IDs in the form: 'MS $Language $Number',
    # e.g. 'MS Hebrew B1' or 'MS Arabic 247'.
    #
    # This looks for the manuscript ID in <idno type="msID">, and warns
    # if it's not as expected.
    #
    # We skip some special cases which are not currently handled by
    # this rule and need more work to fix.
    # We also skip the "minimal-viable-records folder".  These are documents may be of any language,
    # and should be subject to other checks, but the id is not predictable from this folder name
    if relpath.partition("/")[0] in ("Spanish", "Indic", "Greek", "minimum-viable-records"):
        return 0
    actual_manuscript_id = root.find(".//idno[@type='msID']", namespaces=XMLNS).text
    language = os.path.basename(os.path.dirname(relpath))

    # The Fihrist folder is not a language, but is a subfolder under Arabic
    # to contain Arabic documents formatted appropriately for submission to Fihrist
    if language == "Fihrist":
        language = os.path.basename(os.path.dirname(os.path.dirname(relpath)))

    # e.g. Hebrew_B_55.xml ~> B55, Tamil_49.xml ~> 49
    if relpath.startswith("Hebrew/"):
        ms_short_id = "".join(relpath.split(".")[0].rsplit("_")[-2:])
    else:
        ms_short_id = relpath.split("_")[-1].split(".")[0]

    expected_manuscript_id = f"MS {language} {ms_short_id}"
    if expected_manuscript_id != actual_manuscript_id:
        print("")
        print(relpath)
        print(f'\tManuscript ID in <idno type="msID"> is malformed:')
        print(f'\t\tExpected: {GREEN}{expected_manuscript_id!r}{RESET}')
        print(f'\t\tActual:   {RED}{actual_manuscript_id!r}{RESET}')
        return 1
    return 0


def check_keyword_ids(relpath, root, fullpath):
    """
    keyword terms may contain either or both of
    * @ref - an absolute or relative URI
    * @key - an externally defined identifier

    The key attribute is extracted by the Works Pipeline to assign identifiers
    to Concept objects in the resulting Works.

    A common error is to place a `key` value in a `ref` attribute.

    https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-term.html
    https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-keywords.html
    https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-att.canonical.html
    """
    errors = 0
    error_messages = defaultdict(list)
    for term in root.findall(".//keywords//term", namespaces=XMLNS):
        if "ref" in term.attrib:
            ref = term.attrib.get("ref", "").strip()
            if ref == "subject_":
                error_messages[f"ref attribute(s) in {relpath} are effectively empty"] = [(guess_line_label(fullpath, text=f'ref="{ref}"'))]
                errors += 1
            elif ref.startswith("subject_") or ref.startswith("sh"):
                error_messages[f"ref attribute in {relpath} looks like a key"].append(guess_line_label(fullpath, text=f'ref="{ref}"'))
                errors += 1
    if errors:
        for key, value in error_messages.items():
            print(key)
            print("\n".join(value))
    return errors


def check_documents_in_folder(repo_root):
    errors = 0
    for fullpath in sorted(get_file_paths_under(repo_root, suffix=".xml")):
        relpath = os.path.relpath(fullpath, start=repo_root)
        # Exclude a couple of paths that aren't actual TEI files
        if relpath.startswith(("Templates/", "docs/", ".", "venv")):
            continue

        try:
            root = ET.parse(fullpath).getroot()
        except ET.ParseError as err:
            print("")
            print(relpath)

            print(f"\tUnable to parse XML: {err}")
            errors += 1
            continue

        errors += check_author_names(relpath, root, fullpath)
        errors += check_manuscript_id(relpath, root)
        errors += check_keyword_ids(relpath, root, fullpath)
    return errors


def main():
    errors = check_documents_in_folder((
        subprocess.check_output(
            [
                "git",
                "rev-parse",
                "--show-toplevel",
            ]
        )
        .strip()
        .decode("ascii")
    ))
    if errors == 0:
        print(f"{GREEN}🎉 All files checked, no errors!{RESET}")
    else:
        print(
            f"{RED}⚠️ All files checked, {errors} error{'s' if errors > 0 else ''} found!{RESET}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
