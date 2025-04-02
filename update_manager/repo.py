"""Repository Class"""

from abc import ABC, abstractmethod
from argparse import Namespace
from pathlib import Path

from .util import dprint


class Repo(ABC):
    """Repository abstract base class

    This represents one repository in one directory of one type.
    """

    def __init__(self, repo_path: Path, args: Namespace) -> None:
        """Initialize the repository abstract class"""
        dprint(f'"Repo" super-class init routine: dir={repo_path}')
        self.__repo_path = repo_path
        self.__args = args

    @classmethod
    @abstractmethod
    def is_mine(cls, repo_path: Path) -> bool:
        """Is the supplied directory fit my class?"""

    @abstractmethod
    def update(self) -> int:
        """Update this repo"""

    @abstractmethod
    def clean(self) -> int:
        """Clean this repo"""

    @property
    def repo_path(self) -> Path:
        """Return repo_path"""
        return self.__repo_path

    @property
    def args(self) -> Namespace:
        """Return args"""
        return self.__args
