#!/usr/bin/env python3
"""
svn (subversion) Repository Class
"""


import os
import abc

from update_manager.Util import dprint, vprint
from update_manager.Repo import Repo

class SvnRepo(Repo):

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint("SvnRepo init routine repo_dir=%s ..." % self.repo_dir)

    @classmethod
    def is_mine(cls, repo_dir):
        dprint("Looking for '.svn' subdirectory under '%s' ..." % repo_dir)
        return os.path.isdir('%s/.svn' % repo_dir)

    def update(self, stop_on_error=True):
        dprint("svn update (s=%s)" % stop_on_error)
        dprint("NYI: Should run 'svn update' in our directory ...")
        return True

    def clean(self, cleaning_level=1):
        dprint("svn clean (c=%s) is a NOOP" % cleaning_level)
        return True