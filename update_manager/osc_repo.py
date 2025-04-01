"""
OSC Repository Class
"""


import os

from .util import dprint, run_cmd_in_dir
from .repo import Repo


class OscRepo(Repo):
    """Class representing an "osc" repository"""

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint(f'OscRepo init routine repo_dir={self.repo_dir}')

    @classmethod
    def is_mine(cls, repo_dir):
        dprint(f'Looking for ".osc" subdirectory under "{repo_dir}"')
        return os.path.isdir(f'{repo_dir}/.osc')

    def update(self, opts):
        dprint(f'osc update (opts={opts})')
        osc_cmd = ['osc', '-v', 'update'] if opts.verbose else ['osc', 'update']
        return run_cmd_in_dir(self.repo_dir, osc_cmd)

    def clean(self, opts):
        dprint(f'osc clean (level={opts.level}) is a NOOP')
        return 0
