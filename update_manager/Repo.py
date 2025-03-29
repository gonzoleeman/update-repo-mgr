"""
Repository Class
"""


import os
from abc import ABC, abstractmethod

from .Util import dprint


class Repo(ABC):
    """
    Repository abstract base class.

    This represents one repository in one directory of one type.
    """

    def __init__(self, repo_dir):
        dprint("'Repo' super-class init routine ..., dir=%s" % repo_dir)
        self.__repo_dir = repo_dir

    @abstractmethod
    def is_mine(cls, repo_dir):
        """class method: Is the supplied directory 'mine'?"""

    @abstractmethod
    def update(self, opts):
        """Update this repo"""

    @abstractmethod
    def clean(self, cleaning_level=1):
        """clean this repo"""

    @property
    def repo_dir(self):
        """return repo_dir"""
        return self.__repo_dir
