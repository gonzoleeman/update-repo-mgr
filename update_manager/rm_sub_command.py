"""The 'rm' (remove) subcommand"""

from argparse import ArgumentParser, Namespace

from .database import Database, skip_dirs_not_in_db
from .sub_command import SubCommand
from .util import dprint, eprint, print_info


class RmSubCommand(SubCommand):
    """Remove one or more repositories from the database"""

    def __init__(self, database: Database, parser: ArgumentParser, args: Namespace) -> None:
        """Initialize a Rm subcommand instance"""
        SubCommand.__init__(self, database, parser, args)
        dprint(f'"rm" subcommand init routine, args={args}')

    def handle_command(self) -> int:
        """Handle the 'rm' (remove) subcommand

        At least one directory name is expected
        """
        dir_list = self.args.DIRECTORY
        dprint(f'handle_command("rm", dir_list={dir_list}) called')
        dir_list = skip_dirs_not_in_db(dir_list, self.database)
        dprint(f'updated dir_list: {dir_list}')
        result = 0
        for a_dir in dir_list:
            dprint(f'Looking at directory to remove: {a_dir} ...')
            # we do not care if the repo path exists, since we are removing it
            if not self.database.entry_present(a_dir):
                eprint(f'no such entry present: {a_dir}')
                result = 1
                continue
            print_info(f'Removing dir from the DB: {a_dir}')
            self.database.rm_from_list(a_dir)
        return result

    @classmethod
    def add_options(cls, parser: ArgumentParser) -> None:
        """Add appropriate options"""
        parser.add_argument('DIRECTORY',
                            nargs='+',
                            help='Directory to remove')
