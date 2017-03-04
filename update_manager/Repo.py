#!/usr/bin/env python3
"""
Repository Class
"""


import os
import abc

from update_manager.Util import dprint, vprint


class Repo(abc.ABC):
    """
    Repository abstract base class.

    This represents one repository in one directory of one type.
    """

    def __init__(self, repo_dir):
        dprint("'Repo' super-class init routine ..., dir=%s" % repo_dir)
        self.__repo_dir = repo_dir

    @abc.abstractmethod
    def is_mine(cls, repo_dir):
        """class method: Is the supplied directory 'mine'?"""

    @abc.abstractmethod
    def update(self, stop_on_error=True):
        """Update this repo"""

    @abc.abstractmethod
    def clean(self, cleaning_level=1):
        """clean this repo"""

    @property
    def repo_dir(self):
        """return repo_dir"""
        return self.__repo_dir