"""
svn (subversion) Repository Class
"""


import os

from .repo import Repo
from .util import dprint, run_cmd_in_dir


class SvnRepo(Repo):
    """Class representing subversion repositories"""

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint(f'SvnRepo init routine repo_dir={self.repo_dir}')

    @classmethod
    def is_mine(cls, repo_dir):
        dprint(f'Looking for ".svn" subdirectory under "{repo_dir}"')
        res = os.path.isdir('%s/.svn' % repo_dir)
        dprint(f'This is an SVN directory: {res}')
        return res

    def update(self, opts):
        dprint(f'svn update (opts={opts})')
        svn_cmd = ['svn', 'update']
        if opts.quiet:
            svn_cmd.append('-q')
        res = run_cmd_in_dir(self.repo_dir, svn_cmd)
        return res

    def clean(self, opts):
        dprint(f'svn clean (opts={opts}) is a NOOP')
        return 0
