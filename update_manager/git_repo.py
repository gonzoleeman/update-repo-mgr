"""
Git Repository Class
"""

import os

from .util import (
    run_cmd_in_dir,
    run_cmd_in_dir_ret_output,
    dprint,
    )
from .repo import Repo

GIT_CLEAN_LEVEL_1 = 1
GIT_CLEAN_LEVEL_2 = 2


class GitRepo(Repo):
    """Class representing a 'git' repository"""

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint(f'GitRepo init routine repo_dir={self.repo_dir}')

    @classmethod
    def is_mine(cls, repo_dir):
        dprint(f'Looking for ".git" subdirectory under "{repo_dir}"')

        if not os.path.isdir(f'{repo_dir}/.git'):
            dprint('No ".git" subdirectory found')
            return False

        dprint('Checking for remote repository ...')
        (res, cmd_output) = run_cmd_in_dir_ret_output(
            repo_dir,
            ['git', 'remote', 'show'])
        dprint(f'res: {res}')
        dprint(f'cmd_output: "{cmd_output}"')
        if cmd_output:
            dprint('This git repository has a remote')
            return True

        dprint('This git repository is local only -- skipping')

        return False

    def update(self, args):
        dprint(f'git update (args={args})')
        git_cmd = ['git', 'pull', '--all']
        if args.verbose:
            git_cmd.append('-v')
        git_cmd.append('--prune')
        return run_cmd_in_dir(self.repo_dir, git_cmd)

    def clean(self, args):
        dprint(f'git clean (args={args})')
        ret_res = 0
        if args.level > GIT_CLEAN_LEVEL_1:
            git_cmd = ['git', 'remote']
            if args.verbose:
                git_cmd.append('-v')
            git_cmd = [*git_cmd, 'update', '--prune', 'origin']
            res = run_cmd_in_dir(self.repo_dir, git_cmd)
            if res:
                if args.stop_on_error:
                    return res
                ret_res = res
            if args.level > GIT_CLEAN_LEVEL_2:
                git_cmd = ['git', 'prune']
                if not args.verbose:
                    git_cmd.append('-v')
                res = run_cmd_in_dir(self.repo_dir, git_cmd)
                if res:
                    if args.stop_on_error:
                        return res
                    ret_res = res
        git_cmd = ['git', 'gc']
        if args.quiet:
            git_cmd.append('--quiet')
        if args.level > GIT_CLEAN_LEVEL_1:
            git_cmd.append('--aggressive')
        res = run_cmd_in_dir(self.repo_dir, git_cmd)
        if res:
            if args.stop_on_error:
                return res
            ret_res = res
        return ret_res
