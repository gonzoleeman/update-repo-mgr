#!/usr/bin/env python3
"""
The 'update' subcommand
"""

import sys
import os
from optparse import OptionParser

from update_manager.Util import dprint, vprint
from update_manager.repos import update_repo


def handle_update(db, update_args):
    """Handle the 'update' subcommand"""
    dprint("handling 'update' args=%s subcommand" % update_args)

    parser = OptionParser(usage='Usage: %prog [program_options] update OPTIONS')
    parser.add_option('-s', '--stop-on-error', action='store_true',
                      default=False, help='Stop on update errors')
    parser.add_option('-c', '--continue', action='store_true', default=False,
                      help='Continue a previously-interrupted update')
    (options, arguments) = parser.parse_args(update_args)

    if len(arguments) != 0:
        parser.error("No arguments needed")
        sys.exit(1)

    # check for interrupted update in progress
    # if update-in-progress and not continuing then error exit

    for repo_dir in sorted(db.db_dict.keys()):
        repo_type = db.db_dict[repo_dir]
        vprint("Need to update '%s' using '%s'" % (repo_dir, repo_type))
        res = update_repo(repo_dir, repo_type)
        # if error and stop-on-error then stop
        # else mark directory 'k' as 'done'

    # close 'transaction' by removing tracking file
