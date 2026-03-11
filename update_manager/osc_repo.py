"""OSC Repository Class"""

from argparse import Namespace
from pathlib import Path

from .repo import Repo
from .util import dprint, run_command


class OscRepo(Repo):
    """Class representing an "osc" repository"""

    def __init__(self, repo_path: Path, args: Namespace) -> None:
        """Initialize an OscRepo instance"""
        Repo.__init__(self, repo_path, args)
        dprint(f'OscRepo init routine repo_path={self.repo_path}')

    @classmethod
    def is_mine(cls, repo_path: Path) -> bool:
        """Claim this directory if it interests my class"""
        dprint(f'Looking for ".osc" subdirectory under "{repo_path}"')
        osc_subdir_path = repo_path / '.osc'
        return osc_subdir_path.is_dir()

    def update(self) -> int:
        """Update this osc repo"""
        dprint('osc update')
        osc_cmd = 'osc -v update' if self.args.verbose else 'osc update'
        ret = run_command(osc_cmd, cwd=self.repo_path)
        return ret.returncode

    def clean(self) -> int:
        """Clean this osc repo"""
        dprint('osc clean: NOP')
        return 0

    @classmethod
    def get_special_dir(cls) -> str:
        """Return our special directory"""
        return '.osc'
