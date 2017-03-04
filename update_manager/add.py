#!/usr/bin/env python3
"""
The 'add' subcommand
"""

import sys
import os
from optparse import OptionParser

from update_manager.Util import dprint
from update_manager.repos import find_owner


def handle_add(db, add_args):
    """Handle the 'add' subcommand"""
    dprint("handling 'add' args=%s subcommand" % add_args)

    parser = OptionParser(usage='Usage: %prog [program_options] add PATHNAME')
    (options, arguments) = parser.parse_args(add_args)

    if len(arguments) != 1:
        parser.error("Must supply one pathname")
        sys.exit(1)
    arg_supplied = arguments[0]

    # check for interrupted update in progress
    # if update-in-progress print error message and exit

    repo_path = os.path.abspath(arg_supplied)
    if not os.path.isdir(repo_path):
        parser.error("Supplied path must reference a directory: %s" %
                     arg_supplied)
        sys.exit(1)

    if db.entry_present(repo_path):
        print("error: path already present: %s" % repo_path, file=sys.stderr)
        sys.exit(1)

    repo_type = find_owner(repo_path)

    if repo_type is None:
        print("error: unknown repo type: %s" % repo_path, file=sys.stderr)
        sys.exit(1)

    # now finally add it to the list
    db.add_to_list(repo_path, repo_type)
