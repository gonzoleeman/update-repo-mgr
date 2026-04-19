"""Repository Class.

Copyright 2026, Lee Duncan, All Rights Reserved.
"""

from abc import ABC, abstractmethod
from argparse import Namespace
from pathlib import Path


class Repo(ABC):
    """Repository abstract base class.

    This represents one repository in one directory of one type.
    """

    def __init__(self, repo_path: Path, args: Namespace) -> None:
        """Initialize the repository abstract class.

        Arguments:
            repo_path:      the path to the repository
            args:           from option parsing

        """
        self.__repo_path = repo_path
        self.__args = args

    @classmethod
    @abstractmethod
    def is_mine(cls, repo_path: Path) -> bool:
        """Return if this is the supplied directory fit my class."""

    @abstractmethod
    def update(self) -> int:
        """Update this repo."""

    @abstractmethod
    def clean(self) -> int:
        """Clean this repo."""

    @property
    def repo_path(self) -> Path:
        """Return repo_path."""
        return self.__repo_path

    @property
    def args(self) -> Namespace:
        """Return args."""
        return self.__args

    @classmethod
    @abstractmethod
    def get_special_dir(cls) -> str:
        """Return the special directory."""
