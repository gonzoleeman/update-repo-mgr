#!/usr/bin/env python3
"""
Git Repository Class
"""


import os
import abc

from update_manager.Util import dprint, vprint
from update_manager.Repo import Repo

class GitRepo(Repo):

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint("GitRepo init routine repo_dir=%s ..." % self.repo_dir)

    @classmethod
    def is_mine(cls, repo_dir):
        dprint("Looking for '.git' subdirectory under '%s' ..." % repo_dir)
        return os.path.isdir('%s/.git' % repo_dir)

    def update(self, stop_on_error=True):
        dprint("git update (s=%s)" % stop_on_error)
        dprint("NYI: Should run 'git pull -v' in our directory ...")
        return True

    def clean(self, cleaning_level=1):
        dprint("git clean (c=%s)" % cleaning_level)
        dprint("Should run 'git [gc?] ...' in our directory ...")
        return True

