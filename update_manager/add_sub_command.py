"""The 'add' subcommand"""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from .database import Database
from .repos import find_owner
from .sub_command import SubCommand
from .util import dprint, eprint, print_info


class AddSubCommand(SubCommand):
    """Add one or more repositories to the database"""

    def __init__(self, database: Database, parser: ArgumentParser, args: Namespace) -> None:
        """Initialize an add subcommand instance"""
        SubCommand.__init__(self, database, parser, args)
        dprint(f'"add" subcommand init routine, args={args}')

    def handle_command(self) -> int:
        """Handle the 'add' subcommand

        At least one directory name is expected
        """
        dir_list = self.args.DIRECTORY
        dprint(f'handle_command("add", dir_list={dir_list}) called')
        result = 0
        for a_dir in dir_list:
            dprint(f'Looking at directory to add: {a_dir} ...')
            repo_path = Path(a_dir).resolve()
            if not repo_path.is_dir():
                eprint(f'Supplied path must reference a directory: {repo_path}')
                result = 1
                continue
            if self.database.entry_present(repo_path):
                eprint(f'path already present: {repo_path}')
                result = 1
                continue
            repo_type = find_owner(repo_path)
            if repo_type is None:
                eprint(f'error: Unknown or unsupported repo type: {repo_path}')
                result = 1
                continue
            print_info(f'Adding dir to the DB: {repo_path}')
            self.database.add_to_list(repo_path, repo_type)
        return result

    @classmethod
    def add_options(cls, parser: ArgumentParser) -> None:
        """Add appropriate options"""
        parser.add_argument('DIRECTORY',
                            nargs='+',
                            help='Directory to add')
