#!/usr/bin/env python3
"""
The 'rm' (remove) subcommand
"""

import sys
import os
from optparse import OptionParser

from update_manager.Util import dprint


def handle_rm(db, rm_args):
    """Handle the 'rm' (remove) subcommand"""
    dprint("handling 'rm' args=%s subcommand" % rm_args)

    parser = OptionParser(usage='Usage: %prog [program_options] rm PATHNAME')
    (options, arguments) = parser.parse_args(add_args)

    if len(arguments) != 1:
        parser.error("Must supply one pathname")
        sys.exit(1)
    arg_supplied = arguments[0]

    # check for interrupted update in progress
    # if update-in-progress print error message and exit

    repo_path = os.path.abspath(arg_supplied)
    # we do not care if the repo_path exists, since we are removing it

    if not db.entry_present(repo_path):
        print("error: not such entry present: %s" % repo_path, file=sys.stderr)
        sys.exit(1)

    # now finally add it to the list
    db.rm_from_list(repo_path)
