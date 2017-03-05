#!/usr/bin/env python3
"""
The 'list' subcommand
"""

from optparse import OptionParser

from update_manager.Util import dprint
from update_manager.SubCommand import SubCommand


class ListSubCommand(SubCommand):
    def __init__(self, db):
        SubCommand.__init__(self, db, 'list', 'list [options]',
                            'List all of the subcommands.')
        dprint("List subcommand init routine ...")
        self.parser.add_option('-l', '--long', action='store_true',
                               default=False,
                               help='Show repo type as well as directory')

    def handle_command(self, cmd_args):
        dprint("handling 'list' args=%s subcommand" % cmd_args)
        (options, arguments) = self.parser.parse_args(cmd_args)
        self.db.print_list(long=options.long)
