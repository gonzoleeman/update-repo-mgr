#!/usr/bin/env python3
"""
The 'add' subcommand
"""

import sys
import os
from optparse import OptionParser

from update_manager.Util import dprint
from update_manager.repos import find_owner
from update_manager.SubCommand import SubCommand


class AddSubCommand(SubCommand):
    def __init__(self, db):
        SubCommand.__init__(self, db, 'add', 'add [options] REPO-PATH',
                            'Add a repository to the database.')
        dprint("Add subcommand init routine ...")

    def handle_command(self, cmd_args):
        dprint("handling 'add' args=%s subcommand" % cmd_args)
        (options, arguments) = self.parser.parse_args(cmd_args)

        if len(arguments) != 1:
            self.parser.error("Must supply one pathname")
            sys.exit(1)

        arg_supplied = arguments[0]

        # check for interrupted update in progress
        # if update-in-progress print error message and exit

        repo_path = os.path.abspath(arg_supplied)
        if not os.path.isdir(repo_path):
            self.parser.error("Supplied path must reference a directory: %s" %
                         arg_supplied)
            sys.exit(1)

        if self.db.entry_present(repo_path):
            print("error: path already present: %s" % repo_path,
                  file=sys.stderr)
            sys.exit(1)

        repo_type = find_owner(repo_path)

        if repo_type is None:
            print("error: unknown repo type: %s" % repo_path, file=sys.stderr)
            sys.exit(1)

        # now finally add it to the list
        self.db.add_to_list(repo_path, repo_type)
