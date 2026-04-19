"""Git Repository Class.

Copyright 2026, Lee Duncan, All Rights Reserved.
"""

from argparse import Namespace
from pathlib import Path

from .repo import Repo
from .util import dprint, run_command

GIT_CLEAN_LEVEL_1 = 1
GIT_CLEAN_LEVEL_2 = 2


class GitRepo(Repo):
    """Class representing a 'git' repository."""

    def __init__(self, repo_path: Path, args: Namespace) -> None:
        """Initialize an GitRepo instance."""
        Repo.__init__(self, repo_path, args)
        dprint(f'GitRepo init routine repo_path={self.repo_path}, args={args}')

    @classmethod
    def is_mine(cls, repo_path: Path) -> bool:
        """Claim this directory if it interests my class.

        Arguments:
            repo_path: the path to examine

        Returns:
            True on success else False on failure

        """
        dprint(f'Looking for ".git" subdirectory under "{repo_path}"')
        git_subdir_path = repo_path / '.git'
        if not git_subdir_path.is_dir():
            dprint('No ".git" subdirectory found')
            return False
        dprint('Checking for remote repository ...')
        ret = run_command('git remote show', cwd=repo_path)
        dprint(f'command result: {ret.returncode}')
        dprint(f'command output: "{ret.stdout}"')
        if ret.stdout:
            dprint('This git repository has a remote')
            return True
        dprint('This git repository is local only -- skipping')
        return False

    def update(self) -> int:
        """Update this git repo.

        Returns:
            0 on success else non-zero on failure

        """
        dprint('git update')
        git_cmd = 'git pull --all'
        if self.args.verbose:
            git_cmd += ' -v'
        git_cmd += ' --prune'
        ret = run_command(git_cmd, cwd=self.repo_path)
        return ret.returncode

    def __clean_remotes(self) -> int:
        """Clean this repo, but don't go crazy: level 2 cleaning.

        Returns:
            0 on success else non-zero on failure

        """
        git_cmd = 'git remote'
        if self.args.verbose:
            git_cmd += ' -v'
        git_cmd += ' update --prune origin'
        ret = run_command(git_cmd, cwd=self.repo_path)
        return ret.returncode

    def __clean_pruning(self) -> int:
        """Do the pruning: level 3 cleaning.

        Returns:
            0 on success else non-zero on failure

        """
        git_cmd = 'git prune'
        if not self.args.verbose:
            git_cmd += ' -v'
        ret = run_command(git_cmd, cwd=self.repo_path)
        return ret.returncode

    def __clean_gc(self) -> int:
        """Do the garbage collection.

        Returns:
            0 on success else non-zero on failure

        """
        git_cmd = 'git gc'
        if self.args.quiet:
            git_cmd += ' --quiet'
        if self.args.level > GIT_CLEAN_LEVEL_1:
            git_cmd += ' --aggressive'
        ret = run_command(git_cmd, cwd=self.repo_path)
        return ret.returncode

    def clean(self) -> int:
        """Clean this git repo.

        We have 3 levels of cleaning, depending on the 'level'
        argument ('-l'/'--level'), and they are performed in
        the order listed, and given the proper level:

        for level   cleaning
          2         clean remotes
          3         do pruning
         1|3        do garbage cleaning (aggressive if level==3)

        We keep going, if there are errors, unless
        the 'stop_on_error' flag is set

        Returns:
            0 on success else non-zero on failure

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

    @classmethod
    def get_special_dir(cls) -> str:
        """Return our special directory.

        Returns:
            a string that specifies our 'special' directory

        """
        return '.git'
