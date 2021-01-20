#!/usr/bin/env python
# -*- encoding: utf-8
"""
Sync updates to the Arabic manuscripts in fihristorg/fihrist-mss to
wellcometrust/wellcome-collection-tei.

To use this script, you need:

*   Git available on the command-line
*   SSH keys set up to pull from/push to GitHub

You should be able to run this in Python 2 or Python 3, without any
third-party packages.

When it's done, it will open your web browser ready to create a new pull request.

"""

import datetime as dt
import filecmp
import os
import shutil
import subprocess
import tempfile
import webbrowser

try:
    from urllib import urlencode
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlencode, urlunparse


def log(message):
    print("*** %s" % message)


def files_are_equivalent(src, dst):
    if not os.path.exists(dst):
        return False

    if filecmp.cmp(src, dst, shallow=False):
        return True

    with open(src, "rb") as src_f:
        with open(dst, "rb") as dst_f:
            for src_line, dst_line in zip(src_f, dst_f):
                if src_line.rstrip() != dst_line.rstrip():
                    return False

    return True


def copy(src, dst):
    # If the xml file is not already in the Wellcome repository,
    # just copy it straight across.
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
        return

    # Copy in a way that preserves line endings in the dst.
    with open(dst, "rb") as dst_f:
        windows_line_endings = b"\r\n" in dst_f.read()

    shutil.copyfile(src, dst)

    with open(dst, "rb") as dst_f:
        copied_dst = dst_f.read()

    if windows_line_endings:
        copied_dst = copied_dst.replace(b"\n", b"\r\n").replace(b"\r\r\n", b"\r\n")
    else:
        copied_dst = copied_dst.replace(b"\r\n", b"\n")

    with open(dst, "wb") as dst_f:
        dst_f.write(copied_dst)


if __name__ == "__main__":
    working_dir = tempfile.mkdtemp()
    log("Created working directory %s" % working_dir)

    log("Cloning fihristorg/fihrist-mss")
    fihrist_path = os.path.join(working_dir, "fihrist-mss")
    subprocess.check_call([
        "git", "clone",
        "git@github.com:fihristorg/fihrist-mss.git", fihrist_path,
        "--depth", "1"
    ])

    log("Cloning wellcomecollection/wellcome-collection-tei")
    wc_tei_path = os.path.join(working_dir, "wellcome-collection-tei")
    subprocess.check_call([
        "git", "clone",
        "git@github.com:wellcomecollection/wellcome-collection-tei.git", wc_tei_path,
        "--depth", "1"
    ])

    fihrist_arabic_dir = os.path.join(fihrist_path, "collections", "wellcome trust")
    wellcome_arabic_dir = os.path.join(wc_tei_path, "Arabic")

    for name in os.listdir(fihrist_arabic_dir):
        fihrist_xml_path = os.path.join(fihrist_arabic_dir, name)
        wellcome_xml_path = os.path.join(wellcome_arabic_dir, name)

        if not files_are_equivalent(fihrist_xml_path, wellcome_xml_path):
            log("Updating %s" % name)
            copy(fihrist_xml_path, wellcome_xml_path)
            subprocess.check_call(["git", "add", wellcome_xml_path], cwd=wc_tei_path)

    has_changes = subprocess.call(
        ["git", "diff", "--cached", "--exit-code", "--quiet"],
        cwd=wc_tei_path
    )

    if has_changes:
        log("Changes, creating pull request")
        branch = "arabic_ms_updates-%s" % dt.datetime.now().date()
        subprocess.check_call(["git", "checkout", "-b", branch], cwd=wc_tei_path)
        subprocess.check_call([
            "git", "commit", "-m", "Update Arabic manuscripts from fihrist-mss"],
            cwd=wc_tei_path
        )
        subprocess.check_call(["git", "push", "origin", branch], cwd=wc_tei_path)

        wc_tei_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=wc_tei_path).decode("utf8").strip()
        fihrist_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=fihrist_path).decode("utf8").strip()

        query_param = urlencode([
            ("quick_pull", "1"),
            ("body",
             "Updates from %s to https://github.com/fihristorg/fihrist-mss/commit/%s" %
             (wc_tei_commit, fihrist_commit)
            ),
        ])

        github_url = urlunparse((
            "https",
            "github.com",
            "/wellcomecollection/wellcome-collection-tei/compare/master...%s" % branch,
            "",
            query_param,
            ""
        ))
        log("Creating GitHub PR at %s" % github_url)

        webbrowser.open(github_url)

    else:
        log ('no changes, nothing to do')
