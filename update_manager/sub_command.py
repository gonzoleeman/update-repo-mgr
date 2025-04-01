"""
Subcommand class
"""

from abc import ABC, abstractmethod

from .util import dprint


class SubCommand(ABC):
    """
    Subcommand abstract base class
    """

    def __init__(self, database, parser, args):
        dprint('"Subcommand" super-class init routine')
        self.__database = database
        self.__parser = parser
        self.__args = args

    @abstractmethod
    def handle_command(self, short_help=None, long_help=None):
        """Handle the command"""

    @classmethod
    @abstractmethod
    def add_options(cls, parser):
        """Add parser options for this command"""

    @property
    def database(self):
        """Return our database"""
        return self.__database

    @property
    def parser(self):
        """Return our parser"""
        return self.__parser

    @property
    def args(self):
        """Return our args"""
        return self.__args
