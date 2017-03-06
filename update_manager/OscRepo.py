#!/usr/bin/env python3
"""
OSC Repository Class
"""


import os
import abc

from update_manager.Util import dprint, run_cmd_in_dir
from update_manager.Repo import Repo

class OscRepo(Repo):

    def __init__(self, repo_dir):
        Repo.__init__(self, repo_dir)
        dprint("OscRepo init routine repo_dir=%s ..." % self.repo_dir)

    @classmethod
    def is_mine(cls, repo_dir):
        dprint("Looking for '.osc' subdirectory under '%s' ..." % repo_dir)
        res = os.path.isdir('%s/.osc' % repo_dir)
        dprint("This is an OSC directory:", res)
        return res
        
    def update(self, opts):
        dprint("'osc' 'update' (opts=%s)" % opts)
        if opts.verbose:
            osc_cmd = ['osc', '-v', 'update']
        else:
            osc_cmd = ['osc', 'update']
        res = run_cmd_in_dir(self.repo_dir, osc_cmd)
        return res

    def clean(self, cleaning_level=1):
        dprint("osc clean (c=%s) is a NOOP" % cleaning_level)
        return 0
