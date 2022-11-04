import os


RED = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"


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


def check_for_author_names_with_no_original(root, path):
    """
    The front-end expects to see author names in the form:
          <author key="person_88345215">
              <persName xml:lang="eng" type="standard">Badr-addin Muhammad b. Bahram b. Muhammad al-Qalanisi as-Samarqandi</persName>
              <persName xml:lang="ar" type="original">بدر الدين محمد بن بهرام بن محمد القلانسي السمرقندي</persName>
          </author>

    Notice that one is labelled `type="original"`; if this is missing,
    we don't know what contributor to display on the page.
    """
    for author in root.findall(".//{http://www.tei-c.org/ns/1.0}author"):
        persname_nodes = author.findall("./{http://www.tei-c.org/ns/1.0}persName")

        if len(persname_nodes) <= 1:
            continue

        if not any(pn.attrib.get("type") == "original" for pn in persname_nodes):
            message = (
                'Found <author> with multiple <persName> nodes but no type="original"'
            )
            line_label = guess_line_label(
                path, text=persname_nodes[0].text.splitlines()[0]
            )

            if line_label:
                yield f"{message}\n{line_label}"
            else:
                yield message


def check_for_malformed_manuscript_ids(root, path):
    """
    We expect to see manuscript IDs in the form: 'MS $Language $Number',
    e.g. 'MS Hebrew B1' or 'MS Arabic 247'.

    This looks for the manuscript ID in <idno type="msID">, and warns
    if it's not as expected.

    We skip some special cases which are not currently handled by
    this rule and need more work to fix.
    """
    if not ("/Spanish/" in path or "/Indic/" in path or "/Greek/" in path):
        actual_manuscript_id = root.find(
            ".//{http://www.tei-c.org/ns/1.0}idno[@type='msID']"
        ).text

        language = os.path.basename(os.path.dirname(path))

        # e.g. Hebrew_B_55.xml ~> B55, Tamil_49.xml ~> 49
        if "/Hebrew/" in path:
            ms_short_id = "".join(path.split(".")[0].rsplit("_")[-2:])
        else:
            ms_short_id = path.split("_")[-1].split(".")[0]

        expected_manuscript_id = f"MS {language} {ms_short_id}"

        if expected_manuscript_id != actual_manuscript_id:
            yield "\n".join(
                [
                    f'Manuscript ID in <idno type="msID"> is malformed:',
                    f"\tExpected: {GREEN}{expected_manuscript_id!r}{RESET}",
                    f"\tActual:   {RED}{actual_manuscript_id!r}{RESET}",
                ]
            )
