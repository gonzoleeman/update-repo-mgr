"""Subcommand class"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace

from .database import Database
from .util import dprint


class SubCommand(ABC):
    """Subcommand abstract base class"""

    def __init__(self, database: Database, parser: ArgumentParser, args: Namespace) -> None:
        """Initialize instance abstract base class for subcommands"""
        dprint('"Subcommand" super-class init routine')
        self.__database = database
        self.__parser = parser
        self.__args = args

    @abstractmethod
    def handle_command(self) -> int:
        """Handle the command"""

    @classmethod
    @abstractmethod
    def add_options(cls, parser: ArgumentParser) -> None:
        """Add parser options for this command"""

    @property
    def database(self) -> Database:
        """Return our database"""
        return self.__database

    @property
    def parser(self) -> ArgumentParser:
        """Return our parser"""
        return self.__parser

    @property
    def args(self) -> Namespace:
        """Return our args"""
        return self.__args
