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

        res = os.path.isdir('%s/.osc' % repo_dir)
        dprint(f'check for OSC directory returned: {res}')
        return res

    def update(self, opts):
        dprint(f'osc update (opts={opts})')
        if opts.verbose:
            osc_cmd = ['osc', '-v', 'update']
        else:
            osc_cmd = ['osc', 'update']
        res = run_cmd_in_dir(self.repo_dir, osc_cmd)
        return res

    def clean(self, opts):
        dprint(f'osc clean (c={opts.level}) is a NOOP')
        return 0
