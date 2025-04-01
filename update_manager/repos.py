"""
The repository top-level interface. This should be the only place that
knows about individual repo types and abstracts it for others.
"""

from .util import dprint, eprint
from .git_repo import GitRepo
from .svn_repo import SvnRepo
from .osc_repo import OscRepo


# list each repository type we handle, and what object implements it
__REPO_DICT = {
    'git': GitRepo,
    'svn': SvnRepo,
    'osc': OscRepo,
    }


def find_owner(repo_dir):
    """
    Find out which revision control system 'owns' this directory by
    calling each revision object until one of them clains it.
    """
    for (repo_type, repo_obj) in __REPO_DICT.items():
        dprint(f'Looking at repo list entry, type={repo_type}')
        if repo_obj.is_mine(repo_dir):
            dprint(f'Found a match for repo_dir={repo_dir}')
            return repo_type
    return None


def update_repo(repo_dir, repo_type, args):
    """Update a repo"""
    dprint(f'update_repo called ({repo_dir}, {repo_type})')

    repo_obj = __REPO_DICT[repo_type]
    try:
        repo = repo_obj(repo_dir)
        res = repo.update(args)
    except FileNotFoundError:
        eprint(f'directy gone: {repo_dir}. '
               'Consider using the "rm" subcommand to remove it')
        return 1
    dprint(f'update_repo: returning: {res}')
    return res


def clean_repo(repo_dir, repo_type, args):
    """Clean a repo"""
    dprint(f'update_repo called ({repo_dir}, {repo_type})')
    repo_obj = __REPO_DICT[repo_type]
    try:
        repo = repo_obj(repo_dir)
        res = repo.clean(args)
    except FileNotFoundError:
        eprint(f'directy gone: {repo_dir}. ',
               'Consider using the "rm" subcommand to remove it')
        return 1
    return res
