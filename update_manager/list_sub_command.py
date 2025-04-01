"""
The 'list' subcommand
"""

from .util import dprint
from .sub_command import SubCommand


class ListSubCommand(SubCommand):
    """
    List directories being managed
    """
    def __init__(self, database, parser, args):
        SubCommand.__init__(self, database, parser, args)
        dprint(f'List subcommand init routine: args={args}')

    def handle_command(self, short_help=None, long_help=None):
        dprint(f'handle_command("list", "{short_help}", "{long_help}")')
        self.database.print_list(long=self.args.long)

    @classmethod
    def add_options(cls, parser):
        """Add appropriate options"""
        parser.add_argument('-l', '--long',
                            action='store_true',
                            default=False,
                            help='Display repository type as well as directory')
