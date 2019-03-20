"""
Git Repository Class
"""


import os
import abc

from update_manager import opts as global_opts
from update_manager.Util import dprint
from update_manager.Util import run_cmd_in_dir, run_cmd_in_dir_ret_output
from update_manager.Repo import Repo

class GitRepo(Repo):

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint("GitRepo init routine repo_dir=%s ..." % self.repo_dir)

    @classmethod
    def is_mine(cls, repo_dir):
        dprint("Looking for '.git' subdirectory under '%s' ..." % repo_dir)
        if not os.path.isdir('%s/.git' % repo_dir):
            dprint("No '.git' subdirectory found")
            return False
        dprint("Checking for remote repository ...")
        (res, cmd_output) = run_cmd_in_dir_ret_output(repo_dir,
                                                      ['git', 'remote', 'show'])
        dprint("res: ", res)
        dprint("cmd_output: \"%s\"" % cmd_output)
        if cmd_output:
            dprint("This git repository has a remote")
            return True
        dprint("This git repository is local only -- skipping")
        return False

    def update(self, opts):
        dprint("'git' 'update' (opts=%s)" % opts)
        git_cmd = ['git', 'pull', '--all']
        if opts.verbose:
            git_cmd.append('-v')
        git_cmd.append('--prune')
        res = run_cmd_in_dir(self.repo_dir, git_cmd)
        dprint("'update' for git returning:", res)
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
            git_cmd.append('--aggressive')
        res = run_cmd_in_dir(self.repo_dir, git_cmd)
        if res:
            if opts.stop_on_error:
                return res
            ret_res = res
 
        return ret_res

