#!/usr/bin/env python3
"""
The 'rm' (remove) subcommand
"""

import sys
import os
from optparse import OptionParser

from update_manager.Util import dprint
from update_manager.SubCommand import SubCommand


class RmSubCommand(SubCommand):

    def __init__(self, db):
        SubCommand.__init__(self, db, 'rm', 'rm [options] REPO-PATH',
                            'Remove a repository from the database')
        dprint("Rm subcommand init routine ...")

    def handle_command(self, cmd_args):
        """Handle the 'rm' (remove) subcommand"""
        dprint("handling 'rm' args=%s subcommand" % cmd_args)
        (options, arguments) = self.parser.parse_args(cmd_args)

        if len(arguments) != 1:
            parser.error("Must supply one pathname")
            sys.exit(1)
        arg_supplied = arguments[0]

        # check for interrupted update in progress
        # if update-in-progress print error message and exit

        repo_path = os.path.abspath(arg_supplied)
        # we do not care if the repo_path exists, since we are removing it

        if not self.db.entry_present(repo_path):
            print("error: not such entry present: %s" % repo_path,
                  file=sys.stderr)
            sys.exit(1)

        # now finally add it to the list
        self.db.rm_from_list(repo_path)
