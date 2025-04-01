"""
The 'rm' (remove) subcommand
"""

import os

from .util import dprint, print_info, eprint
from .sub_command import SubCommand


class RmSubCommand(SubCommand):
    """
    Remove one or more repositories from the database
    """
    def __init__(self, database, parser, args):
        SubCommand.__init__(self, database, parser, args)
        dprint(f'"rm" subcommand init routine, args={args}')

    def handle_command(self, short_help=None, long_help=None):
        """Handle the 'rm' (remove) subcommand"""
        dprint(f'handle_command("rm", "{short_help}", "{long_help}")')

        dir_list = self.args.DIRECTORY
        dprint(f'directores to remove: {dir_list}')
        result = 0

        # XXX: TODO
        # check for interrupted update in progress
        # if update-in-progress print error message and exit

        for a_dir in dir_list:
            dprint(f'Looking at directory to remove: {a_dir} ...')

            repo_path = os.path.abspath(a_dir)
            # we do not care if the repo_path exists, since we are removing it
            if not self.database.entry_present(repo_path):
                eprint(f'no such entry present: {repo_path}')
                result = 1
                continue

            # now finally remove it from the list
            print_info(f'Removing dir: {repo_path}')
            self.database.rm_from_list(repo_path)

        return result

    @classmethod
    def add_options(cls, parser):
        """Add appropriate optoins"""
        parser.add_argument('DIRECTORY',
                            nargs='+',
                            help='Directory to remove')
