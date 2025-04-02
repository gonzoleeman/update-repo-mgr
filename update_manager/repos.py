"""Top-level interface for all repository classes

This should be the only place that knows about individual
repo types and abstracts it for others.
"""

from argparse import Namespace
from pathlib import Path

from .git_repo import GitRepo
from .osc_repo import OscRepo
from .svn_repo import SvnRepo
from .util import dprint, eprint

# list each repository type we handle, and what object implements it
__REPO_DICT = {
    'git': GitRepo,
    'svn': SvnRepo,
    'osc': OscRepo,
    }


def find_owner(repo_path: Path) -> str | None:
    """Find which revisioin control system owns a repo.

    Find out which revision control system 'owns' this directory by
    calling each revision object until one of them clains it.
    """
    for (repo_type, repo_obj) in __REPO_DICT.items():
        dprint(f'Looking at repo list entry, type={repo_type}')
        # call class method to see if this class wants this directory
        if repo_obj.is_mine(repo_path):
            dprint(f'Found a match for repo_path={repo_path}')
            return repo_type
    return None


def update_repo(repo_path: Path, repo_type: str, args: Namespace) -> int:
    """Update a repo"""
    dprint(f'update_repo called ({repo_path}, {repo_type}, {args})')

    repo_obj = __REPO_DICT[repo_type]
    try:
        repo = repo_obj(repo_path, args)
        res = repo.update()
    except FileNotFoundError:
        eprint(f'directy gone: {repo_path}. '
               'Consider using the "rm" subcommand to remove it')
        return 1
    dprint(f'update_repo: returning: {res}')
    return res


def clean_repo(repo_path: Path, repo_type: str, args: Namespace) -> int:
    """Clean a repo"""
    dprint(f'update_repo called ({repo_path}, {repo_type})')
    repo_obj = __REPO_DICT[repo_type]
    try:
        repo = repo_obj(repo_path, args)
        res = repo.clean()
    except FileNotFoundError:
        eprint(f'directy gone: {repo_path}. ',
               'Consider using the "rm" subcommand to remove it')
        return 1
    return res
