"""
svn (subversion) Repository Class
"""


import os
import abc

from .repo import Repo
from .util import dprint
from .opts import OPTS


class SvnRepo(Repo):

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint(f'SvnRepo init routine repo_dir={self.repo_dir}')

    @classmethod
    def is_mine(cls, repo_dir):
        dprint(f'Looking for ".svn" subdirectory under "{repo_dir}"')
        res = os.path.isdir('%s/.svn' % repo_dir)
        dprint(f'This is an SVN directory: {res}')
        return res

    def update(self, stop_on_error=True):
        dprint(f'svn update (s={stop_on_error})')
        svn_cmd = ['svn', 'update']
        if OPTS.quiet:
            svn_cmd.append('-q')
        res = run_cmd_in_dir(self.repo_dir, svn_cmd)
        return res

    def clean(self, cleaning_level=1):
        dprint(f'svn clean (c={cleaning_level}) is a NOOP')
        return 0
