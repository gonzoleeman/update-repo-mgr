#!/usr/bin/env python3
"""
Git Repository Class
"""


import os
import abc

from update_manager.Util import dprint, run_cmd_in_dir
from update_manager.Repo import Repo
from update_manager import opts

class GitRepo(Repo):

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint("GitRepo init routine repo_dir=%s ..." % self.repo_dir)

    @classmethod
    def is_mine(cls, repo_dir):
        dprint("Looking for '.git' subdirectory under '%s' ..." % repo_dir)
        return os.path.isdir('%s/.git' % repo_dir)

    def update(self, opts):
        dprint("'git' 'update' (opts=%s)" % opts)
        git_cmd = ['git', 'pull']
        if opts.verbose:
            git_cmd.append('-v')
        run_cmd_in_dir(self.repo_dir, git_cmd, stop_on_error=opts.stop_on_error)

    def clean(self, cleaning_level=1):
        dprint("git clean (c=%s)" % cleaning_level)
        dprint("Should run 'git [gc?] ...' in our directory ...")
        return True

