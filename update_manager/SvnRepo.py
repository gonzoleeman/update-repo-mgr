"""
svn (subversion) Repository Class
"""


import os
import abc

from update_manager import opts as global_opts
from update_manager.Util import dprint, run_cmd_in_dir
from update_manager.Repo import Repo

class SvnRepo(Repo):

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint("SvnRepo init routine repo_dir=%s ..." % self.repo_dir)

    @classmethod
    def is_mine(cls, repo_dir):
        dprint("Looking for '.svn' subdirectory under '%s' ..." % repo_dir)
        res = os.path.isdir('%s/.svn' % repo_dir)
        dprint("This is an SVN directory:", res)
        return res

    def update(self, stop_on_error=True):
        dprint("svn update (s=%s)" % stop_on_error)
        svn_cmd = ['svn', 'update']
        if global_opts.quiet:
            svn_cmd.append('-q')
        res = run_cmd_in_dir(self.repo_dir, svn_cmd)
        return res

    def clean(self, cleaning_level=1):
        dprint("svn clean (c=%s) is a NOOP" % cleaning_level)
        return 0
