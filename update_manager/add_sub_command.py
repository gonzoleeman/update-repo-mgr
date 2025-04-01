"""
The 'add' subcommand
"""

import os

from .util import dprint, print_info, eprint
from .repos import find_owner
from .sub_command import SubCommand


class AddSubCommand(SubCommand):
    """
    Add one or more repositories to the database
    """

    def __init__(self, database, parser, args):
        SubCommand.__init__(self, database, parser, args)
        dprint(f'"add" subcommand init routine, args={args}')

    def handle_command(self, short_help=None, long_help=None):
        dprint(f'handling "add" subcommand (dirs={self.args.DIRECTORY})')

        dir_list = self.args.DIRECTORY

        result = 0

        dprint(f'Looking at dir_list={dir_list}')
        for a_dir in dir_list:
            dprint(f'Looking at directory to add: {a_dir} ...')

            repo_path = os.path.abspath(a_dir)
            if not os.path.isdir(repo_path):
                eprint(f'Supplied path must reference a directory: {repo_path}')
                result = 1
                continue

            # XXX: TODO
            # check for interrupted update in progress
            # if update-in-progress print error message and exit

            if self.database.entry_present(repo_path):
                eprint(f'path already present: {repo_path}')
                result = 1
                continue

            repo_type = find_owner(repo_path)

            if repo_type is None:
                eprint(f'error: Unknown or unsupported repo type: {repo_path}')
                result = 1
                continue

            # now finally add it to the list
            print_info(f'Adding dir: {repo_path}')
            self.database.add_to_list(repo_path, repo_type)

        return result

    @classmethod
    def add_options(cls, parser):
        """Add appropriate optoins"""
        parser.add_argument('DIRECTORY',
                            nargs='+',
                            help='Directory to add')
