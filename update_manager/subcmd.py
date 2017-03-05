#!/usr/bin/env python3
"""
Subcommand interface
"""

import sys

from update_manager.Util import dprint

from update_manager.ListSubCommand import ListSubCommand
from update_manager.AddSubCommand import AddSubCommand
from update_manager.RmSubCommand import RmSubCommand
from update_manager.UpdateSubCommand import UpdateSubCommand

__subcmd_dict = {}
__subcmd_dict['list'] = 'ListSubCommand'
__subcmd_dict['add'] = 'AddSubCommand'
__subcmd_dict['rm'] = 'RmSubCommand'
__subcmd_dict['update'] = 'UpdateSubCommand'
# a 'dummy' entry for the 'help' subcommand
__subcmd_dict['help'] = None


def handle_subcmd(db, parser, subcmd, subcmd_args):
    # TODO: throw custom exception of 'subcmd' not in list
    dprint("handle_subcmd(%s, %s): entered" % (subcmd, subcmd_args))
    # handle 'help here, since we can see all the subcommands
    if subcmd == 'help':
        if not subcmd_args:
            parser.print_help()
            sys.exit(0)
        # handle other 'help' options
        help_subcmd = subcmd_args[0]
        if help_subcmd == 'subcommands':
            print_subcmd_list()
            res = 0
        elif subcmd_in_list(help_subcmd):
            # handle subcommand-specific help
            help_subcmd_obj_name = __subcmd_dict[help_subcmd]
            help_subcmd_obj = eval(help_subcmd_obj_name + '(db)')
            help_subcmd_obj.print_help()
            res = 0
        else:
            parser.error("Unknown subcommand help requested")
            res = 1
    else:
        subcmd_obj_name = __subcmd_dict[subcmd]
        subcmd_obj = eval(subcmd_obj_name + '(db)')
        res = subcmd_obj.handle_command(subcmd_args)
    return res

def subcmd_in_list(subcmd):
    return subcmd in __subcmd_dict

def print_subcmd_list():
    print("Subcommand list:")
    for cmd in __subcmd_dict:
        print("\t%s\t%s" % cmd, __subcmd_dict[cmd])
