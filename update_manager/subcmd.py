"""Subcommand interface"""

from argparse import ArgumentParser, Namespace

from .add_sub_command import AddSubCommand
from .clean_sub_command import CleanSubCommand
from .database import Database
from .list_sub_command import ListSubCommand
from .rm_sub_command import RmSubCommand
from .update_sub_command import UpdateSubCommand
from .util import dprint

SUBCMD_DICT = {
    'list': ListSubCommand,
    'add': AddSubCommand,
    'rm': RmSubCommand,
    'update': UpdateSubCommand,
    'clean': CleanSubCommand,
    }


def handle_subcmd(database: Database, parser: ArgumentParser, args: Namespace) -> int:
    """Handle the validated subcommand"""
    subcmd_name = args.subcommand
    dprint(f'handle_subcmd({subcmd_name}): entered')
    # create an instance of our subcommand class
    subcmd_class = SUBCMD_DICT[subcmd_name]
    subcmd = subcmd_class(database, parser, args)
    # let the subcommand class instnace handle the command
    return subcmd.handle_command()
