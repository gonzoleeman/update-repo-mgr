#!/usr/bin/env python3
"""
The 'update' subcommand
"""

import sys
from optparse import OptionParser

from update_manager.Util import dprint, print_info
from update_manager.repos import update_repo
from update_manager.SubCommand import SubCommand


class UpdateSubCommand(SubCommand):
    def __init__(self, db):
        SubCommand.__init__(self, db, 'update', 'update [options]',
                            'Update all repositories in the database.')
        dprint("Update subcommand init routine ...")
        self.parser.add_option('-v', '--verbose', action='store_true',
                               default=False, help='Display more update info')
        self.parser.add_option('-s', '--stop-on-error', action='store_true',
                               default=False, help='Stop on update errors')
        self.parser.add_option('-c', '--continue', action='store_true',
                               default=False,
                               help='Continue a previously-interrupted update')

    def handle_command(self, cmd_args):
        """Handle the 'update' subcommand"""
        dprint("handling 'update' args=%s subcommand" % cmd_args)
        (options, arguments) = self.parser.parse_args(cmd_args)
        dprint("options:", options)
        if len(arguments) != 0:
            parser.error("No arguments needed")
            sys.exit(1)
        # check for interrupted update in progress
        # if update-in-progress and not continuing then error exit
        for repo_dir in sorted(self.db.db_dict.keys()):
            repo_type = self.db.db_dict[repo_dir]
            print_info("Updating '%s' using '%s'" % (repo_dir, repo_type))
            res = update_repo(repo_dir, repo_type, options)
            # if error and stop-on-error then stop
            # else mark directory 'k' as 'done'
        # close 'transaction' by removing tracking file
        # ...
