#!/usr/bin/env python3
"""
The repo top-level interface
"""

from update_manager.Util import dprint
from update_manager.GitRepo import GitRepo
from update_manager.SvnRepo import SvnRepo
from update_manager.OscRepo import OscRepo


repo_dict = {}
repo_dict['git'] = 'GitRepo'
repo_dict['svn'] = 'SvnRepo'
repo_dict['osc'] = 'OscRepo'


def find_owner(repo_dir):
    repo_type = None
    for repo_type in repo_dict:
        obj_name = repo_dict[repo_type]
        dprint("Looking at repo list entry: [%s,%s]" % (obj_name, repo_type))
        if eval(obj_name).is_mine(repo_dir):
            dprint("Found a match!")
            repo_type = repo_type
            break
    return repo_type


def update_repo(repo_dir, repo_type):
    dprint("update_repo called (%s, %s)..." % (repo_dir, repo_type))
    obj = eval(repo_dict[repo_type] + '("' + repo_dir + '")')
    return obj.update()
