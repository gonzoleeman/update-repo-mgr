#!/usr/bin/env python3
"""
OSC Repository Class
"""


import os
import abc

from update_manager.Util import dprint
from update_manager.Repo import Repo

class OscRepo(Repo):

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint("OscRepo init routine repo_dir=%s ..." % self.repo_dir)

    @classmethod
    def is_mine(cls, repo_dir):
        dprint("Looking for '.osc' subdirectory under '%s' ..." % repo_dir)
        return os.path.isdir('%s/.osc' % repo_dir)
        
    def update(self, stop_on_error=True):
        dprint("osc update (s=%s)" % stop_on_error)
        dprint("NYI: Should run 'osc update' in our directory ...")
        return True

    def clean(self, cleaning_level=1):
        dprint("osc clean (c=%s) is a NOOP" % cleaning_level)
        return True
