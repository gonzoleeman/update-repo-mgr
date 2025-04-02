"""Git Repository Class"""

from argparse import Namespace
from pathlib import Path

from .repo import Repo
from .util import dprint, run_cmd_in_dir, run_cmd_in_dir_ret_output

GIT_CLEAN_LEVEL_1 = 1
GIT_CLEAN_LEVEL_2 = 2


class GitRepo(Repo):
    """Class representing a 'git' repository"""

    def __init__(self, repo_path: str, args: Namespace) -> None:
        """Initialize an GitRepo instance"""
        Repo.__init__(self, repo_path, args)
        dprint(f'GitRepo init routine repo_path={self.repo_path}, args={args}')

    @classmethod
    def is_mine(cls, repo_path: Path) -> bool:
        """Claim this directory if it interests my class"""
        dprint(f'Looking for ".git" subdirectory under "{repo_path}"')
        git_subdir_path = repo_path / '.git'
        if not git_subdir_path.is_dir():
            dprint('No ".git" subdirectory found')
            return False
        dprint('Checking for remote repository ...')
        (res, cmd_output) = run_cmd_in_dir_ret_output(repo_path,
                                                      ['git', 'remote', 'show'])
        dprint(f'command result: {res}')
        dprint(f'command output: "{cmd_output}"')
        if cmd_output:
            dprint('This git repository has a remote')
            return True
        dprint('This git repository is local only -- skipping')
        return False

    def update(self) -> int:
        """Update this git repo"""
        dprint('git update')
        git_cmd = ['git', 'pull', '--all']
        if self.args.verbose:
            git_cmd.append('-v')
        git_cmd.append('--prune')
        return run_cmd_in_dir(self.repo_path, git_cmd)

    def __clean_remotes(self) -> int:
        """Clean this repo, but don't go crazy: level 2 cleaning"""
        git_cmd = ['git', 'remote']
        if self.args.verbose:
            git_cmd.append('-v')
        git_cmd = [*git_cmd, 'update', '--prune', 'origin']
        return run_cmd_in_dir(self.repo_path, git_cmd)

    def __clean_pruning(self) -> int:
        """Do the pruning: level 3 cleaning"""
        git_cmd = ['git', 'prune']
        if not self.args.verbose:
            git_cmd.append('-v')
        return run_cmd_in_dir(self.repo_path, git_cmd)

    def __clean_gc(self) -> int:
        """Do the garbage collection"""
        git_cmd = ['git', 'gc']
        if self.args.quiet:
            git_cmd.append('--quiet')
        if self.args.level > GIT_CLEAN_LEVEL_1:
            git_cmd.append('--aggressive')
        return run_cmd_in_dir(self.repo_path, git_cmd)

    def clean(self) -> int:
        """Clean this git repo

        We have 3 levels of cleaning, depending on the 'level'
        argument ('-l'/'--level'), and they are performed in
        the order listed, and given the proper level:

        for level   cleaning
          2         clean remotes
          3         do pruning
         1|3        do garbage cleaning (aggressive if level==3)

        We keep going, if there are errors, unless
        the 'stop_on_error' flag is set
        """
        dprint('git clean')
        return_res = 0
        if self.args.level > GIT_CLEAN_LEVEL_1:
            res = self.__clean_remotes()
            if res:
                if self.args.stop_on_error:
                    return res
                return_res = res
            if self.args.level > GIT_CLEAN_LEVEL_2:
                res = self.__clean_pruning()
                if res:
                    if self.args.stop_on_error:
                        return res
                    return_res = res
        res = self.__clean_gc()
        if res:
            if self.args.stop_on_error:
                return res
            return_res = res
        return return_res
