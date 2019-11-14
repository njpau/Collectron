#!/usr/bin/env python

"""

This program generates Tesira version information in various formats, and based on:

- The output of 'git describe' for the currently checked out branch.

- The current user name

- The BIAMP_BUILD_TYPE environment variable (Release, Beta or Development)

- The name of the currently checked out branch.

"""

import subprocess

import re

import getpass

import sys

import os

 

def getVersions():

    """

    Runs 'git describe' on the currently checked out branch and parses the output to determine the major/minor/revision

    numbers and trailer (commits since release tag and short hash).

    """

 

    description = subprocess.check_output(['git', 'describe', '--tags', '--match', '[0-9]*'])

    m = re.match('(?P<major>[0-9]*)\.(?P<minor>[0-9]*)\.(?P<revision>[0-9]*)-(?P<trailer>.*$)', description)

 

    if not m:

        print("Unable to find a sensible version number in output of git describe: {}".format(description))

        sys.exit(1)

 

    major = m.group('major')

    minor = m.group('minor')

    revision = m.group('revision')

    trailer = m.group('trailer')

 

    return (major, minor, revision, trailer)

 

def getUser():

    """

    Returns the name of the current user or 'unknown' if it cannot be determined.

    """

    return getpass.getuser() or 'unknown'

 

def getBuildType():

    """

    Returns the build type (release, beta or dev) by inspecting the BIAMP_BUILD_TYPE environment variable.

    """

    buildtype = os.environ.get('BIAMP_BUILD_TYPE') or ''

    buildtype = buildtype.lower()

 

    if buildtype not in ('release', 'beta'):

        buildtype = 'dev'

 

    return buildtype

 

def getBranch():

    """

    Returns the currently checked out Git branch, or "unkown" if it cannot be determined.

    """

    branch = subprocess.check_output(['git', 'symbolic-ref', '--short', '-q', 'HEAD']).strip() or 'unknown'

    return branch

 

 

(major, minor, revision, trailer) = getVersions()

branch = getBranch()

user = getUser()

buildtype = getBuildType()

 

identifier = "{}-{}.{}.{}-{}".format(buildtype, major, minor, revision, trailer)

 

# If it is a development build, add branch and user to the build identifier.

if buildtype == 'dev':

    identifier += "-{}-{}".format(user, branch)

 

# Parse the commmand line arguments

import argparse

parser = argparse.ArgumentParser(description="Determines Tesira version information and outputs it in various formats.")

parser.add_argument('--cpp', metavar='cpp_file', nargs=1, help="Write version information to the given file in C++ format")

args = parser.parse_args()

 

if not args.cpp:

     # Just print the version in the form major.minor.revision and exit.

     print("{}.{}.{}.{}".format(major, minor, revision, 0))

     sys.exit(0)

 

# CPP file output has been requested.

outfile = args.cpp[0]

 

# Create the new text for the CPP file.

cppnew = '''#include "Serialize.h"

 

namespace ReleaseVersion

{{

    extern const uint32_t RELEASE_VERSION_MAJOR = {};

    extern const uint32_t RELEASE_VERSION_MINOR = {};

    extern const uint32_t RELEASE_VERSION_DOT = {};

    extern const uint32_t RELEASE_VERSION_BUILD = 0;

    extern const Serialize::SerializableString BUILD_IDENTIFIER = "{}";

}} // namespace ReleaseVersion'''.format(major, minor, revision, identifier)

 

# Read the current text from the CPP file.

try:

    with open(outfile, "r") as f:

        cpporiginal = f.read()

except IOError:

    cpporiginal = ''

      

# Update the CPP file only if the text has changed.

# This prevents make from thinking that the file has changed and therefore recompiling it unnecessarily.

if (cpporiginal != cppnew):

    print("Updating Tesira version information in {}".format(outfile))

    with open(outfile, "w") as f:

        f.write(cppnew)
