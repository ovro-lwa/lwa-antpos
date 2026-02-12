# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# This file is placed into the public domain.

# Calculates the current version number.  If possible, this is the
# output of “git describe”, modified to conform to the versioning
# scheme that setuptools uses.  If “git describe” returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the RELEASE-VERSION file.
#
# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import *
#
# setup(
#     version=get_git_version(),
#     .
#     .
#     .
# )
#
#
# This will automatically update the RELEASE-VERSION file, if
# necessary.  Note that the RELEASE-VERSION file should *not* be
# checked into git; please add it to your top-level .gitignore file.
#
# You'll probably want to distribute the RELEASE-VERSION file in your
# sdist tarballs; to do this, just create a MANIFEST.in file that
# contains the following line:
#
#   include RELEASE-VERSION

__all__ = ("get_git_version")

import re
from subprocess import Popen, PIPE


def _git_describe_to_pep440(version_str):
    """Convert git-describe output to a PEP 440 compliant version.

    Examples:
        "0.6.12" -> "0.6.12"
        "0.6.12-7-g66581a2" -> "0.6.12.post7+g66581a2"
        "0.6.12-7-g66581a2-dirty" -> "0.6.12.post7+g66581a2.dirty"
    """
    if not version_str or version_str is None:
        return None
    version_str = version_str.strip()
    # Strip -dirty so we can handle it separately
    dirty = False
    if version_str.endswith("-dirty"):
        version_str = version_str[:-6]  # len("-dirty") == 6
        dirty = True
    # Match tag-N-gSHORT_HASH (e.g. 0.6.12-7-g66581a2)
    match = re.match(r"^(.+)-(\d+)-g([a-f0-9]+)$", version_str)
    if match:
        tag, commits, short_hash = match.groups()
        # PEP 440: use .postN for commits after tag, + for local version
        pep440 = "{}.post{}+{}".format(tag, commits, short_hash)
        if dirty:
            pep440 += ".dirty"
        return pep440
    # Plain tag (e.g. 0.6.12) or unknown format: return as-is if no dirty
    if dirty:
        version_str = version_str + "+dirty"
    return version_str


def call_git_describe(abbrev):
    try:
        p = Popen(
            ['git', 'describe', '--abbrev=%d' % abbrev],
            stdout=PIPE,
            stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()

    except:
        return None


def is_dirty():
    try:
        p = Popen(["git", "diff-index", "--name-only", "HEAD"],
                  stdout=PIPE,
                  stderr=PIPE)
        p.stderr.close()
        lines = p.stdout.readlines()
        return len(lines) > 0
    except:
        return False


def read_release_version():
    try:
        f = open("RELEASE-VERSION", "r")

        try:
            version = f.readlines()[0]
            return version.strip()

        finally:
            f.close()

    except:
        return None


def write_release_version(version):
    f = open("RELEASE-VERSION", "w")
    f.write("%s\n" % version)
    f.close()


def get_git_version(abbrev=7):
    # Read in the version that's currently in RELEASE-VERSION.

    release_version = read_release_version()

    # First try to get the current version using “git describe”.

    raw = call_git_describe(abbrev)
    if raw is not None:
        version = raw.decode("UTF-8").strip()
        if is_dirty():
            version += "-dirty"
        version = _git_describe_to_pep440(version)
    else:
        version = None

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION (and normalize it to PEP 440 if needed).
    if version is None:
        version = _git_describe_to_pep440(release_version) if release_version else None

    # If we still don't have anything, that's an error.
    if version is None:
        raise ValueError("Cannot find the version number!")

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
    if version != release_version:
        write_release_version(version)

    # Finally, return the current version (PEP 440 compliant).
    return version


if __name__ == "__main__":
    print( get_git_version())
