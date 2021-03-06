"""
The repository top-level interface. This should be the only place that
knows about individual repo types and abstracts it for others.
"""

import sys

from update_manager.Util import dprint, eprint
from update_manager.GitRepo import GitRepo
from update_manager.SvnRepo import SvnRepo
from update_manager.OscRepo import OscRepo


# list each repository type we handle, and what object implements it
__repo_dict = {}
__repo_dict['git'] = 'GitRepo'
__repo_dict['svn'] = 'SvnRepo'
__repo_dict['osc'] = 'OscRepo'


def find_owner(repo_dir):
    """
    Find out which revision control system 'owns' this directory by
    calling each revision object until one of them clains it.
    """
    repo_match = None
    for repo_type in __repo_dict:
        repo_obj_name = __repo_dict[repo_type]
        dprint("Looking at repo list entry: [%s,%s]" %
               (repo_obj_name, repo_type))
        if eval(repo_obj_name).is_mine(repo_dir):
            dprint("Found a match for repo_dir=", repo_dir)
            repo_match = repo_type
            break
    return repo_match

def update_repo(repo_dir, repo_type, opts):
    dprint("update_repo called (%s, %s)..." % (repo_dir, repo_type))
    repo_obj_name = __repo_dict[repo_type]
    try:
        repo_obj = eval(repo_obj_name + '("' + repo_dir + '")')
        res = repo_obj.update(opts)
    except FileNotFoundError:
        eprint("directy gone: %s. " % repo_dir +
               "Consider using the 'rm' subcommand to remove it")
        return 1
    dprint("update_repo: returning:", res)
    return res

def clean_repo(repo_dir, repo_type, opts):
    dprint("update_repo called (%s, %s)..." % (repo_dir, repo_type))
    repo_obj_name = __repo_dict[repo_type]
    repo_obj = eval(repo_obj_name + '("' + repo_dir + '")')
    res = repo_obj.clean(opts)
    return res
