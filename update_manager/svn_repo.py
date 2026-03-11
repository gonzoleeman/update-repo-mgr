"""svn (subversion) Repository Class"""

from argparse import Namespace
from pathlib import Path

from .repo import Repo
from .util import dprint, run_command


class SvnRepo(Repo):
    """Class representing subversion repositories"""

    def __init__(self, repo_path: Path, args: Namespace) -> None:
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
        svn_cmd = 'svn update -v' if self.args.quiet else 'svn update'
        ret = run_command(svn_cmd, cwd=self.repo_path)
        return ret.returncode

    def clean(self) -> int:
        """Update this svn repo (NOP)"""
        dprint('svn clean: NOP')
        return 0

    @classmethod
    def get_special_dir(cls) -> str:
        """Return our special directory"""
        return '.svn'
