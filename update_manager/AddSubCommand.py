"""
The 'add' subcommand
"""

import sys
import os
from optparse import OptionParser

from update_manager.Util import dprint, print_info, eprint
from update_manager.repos import find_owner
from update_manager.SubCommand import SubCommand


class AddSubCommand(SubCommand):
    def __init__(self, db):
        SubCommand.__init__(self, db, 'add', 'add [options] [REPO-PATH]',
                            'Add a repository to the database.')
        dprint("Add subcommand init routine ...")

    def handle_command(self, cmd_args):
        dprint("handling 'add' args=%s subcommand" % cmd_args)
        (options, arguments) = self.parser.parse_args(cmd_args)

        if not arguments:
            # use default of current working directory
            repo_path = os.getcwd()
        elif len(arguments) == 1:
            arg_supplied = arguments.pop()
            repo_path = os.path.abspath(arg_supplied)
            if not os.path.isdir(repo_path):
                self.parser.error(\
                    "Supplied path must reference a directory: %s" %
                    arg_supplied)
                sys.exit(1)
        else:
            self.parser.error("Must supply one pathname max")
            sys.exit(1)

        # check for interrupted update in progress
        # if update-in-progress print error message and exit

        if self.db.entry_present(repo_path):
            eprint("path already present: %s" % repo_path)
            sys.exit(1)

        repo_type = find_owner(repo_path)

        if repo_type is None:
            eprint("error: Unknown or unsupported repo type: %s" %
                   repo_path)
            sys.exit(1)

        # now finally add it to the list
        print_info("Adding dir: " + repo_path)
        self.db.add_to_list(repo_path, repo_type)
