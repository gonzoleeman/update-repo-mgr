"""svn (subversion) Repository Class"""

from argparse import Namespace
from pathlib import Path

from .repo import Repo
from .util import dprint, run_cmd_in_dir


class SvnRepo(Repo):
    """Class representing subversion repositories"""

    def __init__(self, repo_path: str, args: Namespace) -> None:
        """Initialize an SvnRepo instance"""
        Repo.__init__(self, repo_path, args)
        dprint(f'SvnRepo init routine repo_path={self.repo_path}')

    @classmethod
    def is_mine(cls, repo_path: Path) -> bool:
        """Claim this directory if it interests my class"""
        dprint(f'Looking for ".svn" subdirectory under "{repo_path}"')
        svn_subdir_path = repo_path / '.svn'
        return svn_subdir_path.is_dir()

    def update(self) -> int:
        """Update this svn repo (NOP)"""
        dprint('svn update')
        svn_cmd = ['svn', 'update']
        if self.opts.quiet:
            svn_cmd.append('-q')
        return run_cmd_in_dir(self.repo_path, svn_cmd)

    def clean(self) -> int:
        """Update this svn repo (NOP)"""
        dprint('svn clean: NOP')
        return 0
