"""
Subcommand interface
"""

import sys

from .Util import dprint
from .SubCommand import SubCommand
from .ListSubCommand import ListSubCommand
from .AddSubCommand import AddSubCommand
from .RmSubCommand import RmSubCommand
from .UpdateSubCommand import UpdateSubCommand
from .CleanSubCommand import CleanSubCommand


SUBCMD_DICT = {
    'list' : 'ListSubCommand',
    'add' : 'AddSubCommand',
    'rm' : 'RmSubCommand',
    'update' : 'UpdateSubCommand',
    'clean' : 'CleanSubCommand',
    'help' : 'HelpSubCommand',
    }


class HelpSubCommand(SubCommand):
    def __init__(self, db):
        SubCommand.__init__(self, db, 'help',
                            'help [options] [subcommands|cmd]',
                            'Print help information')
        dprint("Help subcommand init routine ...")

    def handle_command(self, cmd_args):
        dprint("handling 'help' args=%s subcommand" % cmd_args)
        (options, arguments) = self.parser.parse_args(cmd_args)
        # the 'help' with no argument case was already handled
        if len(arguments) != 1:
            self.parser.error("too many arguments")
            sys.exit(1)
        help_subcmd = cmd_args[0]
        dprint("Help subcommand: ", help_subcmd)
        # handle subcommand-specific help
        help_subcmd_obj_name = SUBCMD_DICT[help_subcmd]
        dprint("obj name: ", help_subcmd_obj_name)
        help_subcmd_obj = eval(help_subcmd_obj_name + '(self.db)')
        help_subcmd_obj.print_help()
        return 0

def handle_subcmd(db, parser, subcmd, subcmd_args):
    # TODO: throw custom exception of 'subcmd' not in list
    dprint("handle_subcmd(%s, %s): entered" % (subcmd, subcmd_args))
    # handle special cases for 'help' here
    if subcmd == 'help':
        if not subcmd_args:
            parser.print_help()
            sys.exit(0)
        if subcmd_args == ['subcommands']:
            print_subcmd_list(db)
            sys.exit(0)
        elif not subcmd_in_list(subcmd_args[0]):
            parser.error("Unknown subcommand help requested")
            sys.exit(1)
    subcmd_obj_name = SUBCMD_DICT[subcmd]
    subcmd_obj = eval(subcmd_obj_name + '(db)')
    return subcmd_obj.handle_command(subcmd_args)

def subcmd_in_list(subcmd):
    return subcmd in SUBCMD_DICT

def print_subcmd_list(db):
    print("Subcommand list:")
    for subcmd in SUBCMD_DICT:
        if subcmd == 'help':
            help_msg = 'Print help information.'
        else:
            subcmd_obj_name = SUBCMD_DICT[subcmd]
            subcmd_obj = eval(subcmd_obj_name + '(db)')
            help_msg = subcmd_obj.long_help
        print("\t%s\t%s" % (subcmd, help_msg))
