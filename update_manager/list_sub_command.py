"""The 'list' subcommand"""

from argparse import ArgumentParser, Namespace

from .database import Database
from .sub_command import SubCommand
from .util import dprint


class ListSubCommand(SubCommand):
    """List directories being managed"""

    def __init__(self, database: Database, parser: ArgumentParser, args: Namespace) -> None:
        """Initialize list subcommand instance"""
        SubCommand.__init__(self, database, parser, args)
        dprint(f'List subcommand init routine: args={args}')

    def handle_command(self) -> None:
        """Handle the 'list' subcommand

        No directory names are expected
        """
        dprint('handle_command("list")')
        if self.args.long:
            self.database.print_list_long()
        else:
            self.database.print_list_short()

    @classmethod
    def add_options(cls, parser: ArgumentParser) -> None:
        """Add appropriate options"""
        parser.add_argument('-l', '--long',
                            action='store_true',
                            default=False,
                            help='Display repository type as well as directory')
