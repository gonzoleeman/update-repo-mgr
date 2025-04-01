"""
Repository Class
"""


from abc import ABC, abstractmethod

from .util import dprint


class Repo(ABC):
    """
    Repository abstract base class.

    This represents one repository in one directory of one type.
    """

    def __init__(self, repo_dir):
        dprint(f'"Repo" super-class init routine ..., dir={repo_dir}')
        self.__repo_dir = repo_dir

    @classmethod
    @abstractmethod
    def is_mine(cls, repo_dir):
        """class method: Is the supplied directory 'mine'?"""

    @abstractmethod
    def update(self, opts):
        """Update this repo"""

    @abstractmethod
    def clean(self, opts):
        """clean this repo"""

    @property
    def repo_dir(self):
        """return repo_dir"""
        return self.__repo_dir
