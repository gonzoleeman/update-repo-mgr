"""
Subcommand class
"""

from abc import ABC, abstractmethod

from .util import dprint


class SubCommand(ABC):
    """
    Subcommand abstract base class
    """

    def __init__(self, db, parser, args):
        dprint(f'"Subcommand" super-class init routine')
        self.__db = db
        self.__parser = parser
        self.__args = args

    @abstractmethod
    def handle_command(self, short_help=None, long_help=None):
        """Handle the command"""

    @classmethod
    def add_options(cls, parser):
        """Add parser options for this command"""
        print('DEBUG: class-level "add_options" called (%s)!' % \
              cls.__name__)

    @property
    def db(self):
        return self.__db

    @property
    def parser(self):
        return self.__parser

    @property
    def args(self):
        return self.__args
