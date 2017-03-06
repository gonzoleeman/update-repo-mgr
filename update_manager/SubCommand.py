#!/usr/bin/env python3
"""
Subcommand class
"""

import os
import abc
from optparse import OptionParser

from update_manager.Util import dprint

class SubCommand(abc.ABC):
    """
    Subcommand abstract base class
    """

    def __init__(self, db, command_name, short_help, long_help):
        dprint("'Subcommand' super-class init routine, cmd=%s" % command_name)
        self.__db = db
        self.__command_name = command_name
        self.__short_help = short_help
        self.__long_help = long_help
        self.setup_parser()

    def setup_parser(self):
        """Set up a parser ready to go"""
        self.__parser = OptionParser(
            usage='Usage: %%prog [program_options] %s' % self.__short_help)

    @abc.abstractmethod
    def handle_command(self, db, cmd_args):
        """Handle the command"""

    def print_help(self):
        """Print help information for this subcommand"""
        self.__parser.print_help()

    @property
    def db(self):
        return self.__db

    @property
    def command_name(self):
        return self.__command_name

    @property
    def short_help(self):
        return self.__short_help

    @property
    def long_help(self):
        return self.__long_help

    @property
    def parser(self):
        return self.__parser