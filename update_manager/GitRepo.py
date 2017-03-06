#!/usr/bin/env python3
"""
Git Repository Class
"""


import os
import abc

from update_manager import opts as global_opts
from update_manager.Util import dprint, run_cmd_in_dir
from update_manager.Repo import Repo

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
        res = run_cmd_in_dir(self.repo_dir, git_cmd)
        return res

    def clean(self, opts):
        dprint("git clean (opts=%s)" % opts)

        ret_res = 0

        if opts.level > 1:
            git_cmd = ['git', 'remote']
            if opts.verbose:
                git_cmd.append('-v')
            git_cmd = git_cmd + ['update', '--prune', 'origin']
            res = run_cmd_in_dir(self.repo_dir, git_cmd)
            if res:
                if opts.stop_on_error:
                    return res
                ret_res = res

            if opts.level > 2:
                git_cmd = ['git', 'prune']
                if not opts.verbose:
                    git_cmd.append('-v')
                res = run_cmd_in_dir(self.repo_dir, git_cmd)
                if res:
                    if opts.stop_on_error:
                        return res
                    ret_res = res

        git_cmd = ['git', 'gc']
        if global_opts.quiet:
            git_cmd.append('--quiet')
        if opts.level > 1:
            git_cmd.append('--agressive')
        res = run_cmd_in_dir(self.repo_dir, git_cmd)
        if res:
            if opts.stop_on_error:
                return res
            ret_res = res
 
        return ret_res

