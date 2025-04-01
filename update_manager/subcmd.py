"""
Subcommand interface
"""

import sys

from .util import dprint, eprint

from .sub_command import SubCommand
from .list_sub_command import ListSubCommand
from .add_sub_command import AddSubCommand
from .rm_sub_command import RmSubCommand
from .update_sub_command import UpdateSubCommand
from .clean_sub_command import CleanSubCommand


SUBCMD_DICT = {
    'list' : ListSubCommand,
    'add' : AddSubCommand,
    'rm' : RmSubCommand,
    'update' : UpdateSubCommand,
    'clean' : CleanSubCommand,
    }


def handle_subcmd(db, parser, args):
    subcmd_name = args.subcommand

    dprint(f'handle_subcmd({subcmd_name}): entered')

    # create an instance of our subcommand class
    subcmd_class = SUBCMD_DICT[subcmd_name]
    subcmd = subcmd_class(db, parser, args)

    # let the subcommand class instnace handle the command
    return subcmd.handle_command()
