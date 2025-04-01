"""
The 'list' subcommand
"""

from .util import dprint
from .sub_command import SubCommand


class ListSubCommand(SubCommand):
    """
    List directories being managed
    """
    def __init__(self, db, parser, args):
        SubCommand.__init__(self, db, parser, args)
        dprint(f'List subcommand init routine: args={args}')

    def handle_command(self):
        dprint('handling "list" subcommand')
        self.db.print_list(long=self.args.long)

    @classmethod
    def add_options(cls, parser):
        """Add appropriate options"""
        parser.add_argument('-l', '--long',
                            action='store_true',
                            default=False,
                            help='Display repository type as well as directory')
