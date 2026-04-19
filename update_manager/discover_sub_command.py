"""The 'discover' subcommand.

Copyright 2026, Lee Duncan, All Rights Reserved.
"""

import re
from argparse import ArgumentParser, Namespace
from os import walk
from pathlib import Path

from .database import Database
from .repos import find_owner, get_repo_special_dir_names
from .sub_command import SubCommand
from .util import dprint, print_info, print_multiline_info


class DiscoverSubCommand(SubCommand):
    """Discover all currently-unknown repos under a given directory."""

    def __init__(self, database: Database, parser: ArgumentParser, args: Namespace) -> None:
        """Initialize discover subcommand."""
        SubCommand.__init__(self, database, parser, args)
        dprint(f'"discover" subcommand init routine, args={args}')

    def handle_command(self) -> int:
        """Handle the 'discover' subcommand.

        Returns:
            0 for success, else 1

        """
        dir_to_use = self.args.DIRECTORY
        dprint(f'handle_command("discover", dir_to_use={dir_to_use}) called')
        dprint(f'Discover: Looking under directory {dir_to_use}')
        skip_patch_pat = match_patch_pat = None
        if self.args.skip_patch:
            if self.args.match_patch:
                self.parser.error('Cannot specify "match" and "skip" at the same time')
            dprint(fr'Compiling skip pattern: {self.args.skip_patch} ...')
            try:
                skip_patch_pat = re.compile(self.args.skip_patch)
            except re.error as e:
                self.parser.error(f'Illegal skip pattern ({e}): "{self.args.skip_patch}"')
                return 1
        elif self.args.match_patch:
            dprint(fr'Compiling match pattern: {self.args.match_patch} ...')
            try:
                match_patch_pat = re.compile(self.args.match)
            except re.error as e:
                self.parser.error(f'Illegal match pattern ({e}): "{self.args.match}"')
                return 1
        skip_dir_pat = None
        if self.args.skip_dir:
            dprint(fr'Compiling skip dir patttern: {self.args.skip_dir} ...')
            try:
                skip_dir_pat = re.compile(self.args.skip_dir)
            except re.error as e:
                self.parser.error(f'Illegal match pattern ({e}): "{self.args.match}"')
                return 1
        # get a list of known special dirs (speed up checking)
        spcl_dirs = get_repo_special_dir_names()
        dprint(f'special directory list: {spcl_dirs}')
        ttl_discovered = ttl_already_known = ttl_skipped = 0
        for a_dir, sub_dirs, files_found in walk(dir_to_use):
            dprint(f'Looking at directory to add: {a_dir} ...')
            repo_path = Path(a_dir).resolve()
            if self.database.entry_present(str(repo_path)):
                print_info(f'skipping path already present: {repo_path}')
                sub_dirs[:] = []
                ttl_already_known += 1
                continue
            # check the path if needed
            if skip_dir_pat and skip_dir_pat.search(str(repo_path)):
                dprint(f'Skipping {repo_path}: "SKIP DIRECTORY" match!')
                ttl_skipped += 1
                sub_dirs[:] = []
                continue
            # skip this if none of the subdirs are in the special list
            if not list(set(spcl_dirs) & set(sub_dirs)):
                dprint('skipping: no special directories here!')
                ttl_skipped += 1
                continue
            # skip directories where there are no files
            if not files_found:
                dprint('skipping: no files in this directory!')
                ttl_skipped += 1
                continue
            # skip if requested to filter, by user
            if skip_patch_pat and skip_patch_pat.search(a_dir):
                dprint(f'Skipping {a_dir}: "SKIP" pattern match!')
                ttl_skipped += 1
                sub_dirs[:] = []
                continue
            if match_patch_pat and not match_patch_pat.search(a_dir):
                dprint(f'Skipping {a_dir}: does not MATCH pattern!')
                ttl_skipped += 1
                continue
            # see if this is actually a repo
            repo_type = find_owner(repo_path)
            if repo_type is None:
                dprint(f'Unknown or unsupported repo type: {repo_path}')
                ttl_skipped += 1
                continue
            # this is a repo dir
            sub_dirs[:] = []
            print_info(f'Adding dir to the DB: {repo_path}')
            self.database.add_to_list(repo_path, repo_type)
            ttl_discovered += 1

        if not self.args.quiet:
            report_arr = [
                '"Discover" Summary Report',
                '',
                f' Directories Discovered:    {ttl_discovered:6d}',
                f' Directories Already Known: {ttl_already_known:6d}',
                f' Directories Skipped:       {ttl_skipped:6d}',
                ]
            print_multiline_info(report_arr)

        return 0

    @classmethod
    def add_options(cls, parser: ArgumentParser) -> None:
        """Add options for the "clean" subcommand."""
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            default=False,
                            help='Discover verbosely')
        parser.add_argument('-m', '--match-patch',
                            default=None,
                            help='Filename pattern to match')
        parser.add_argument('-s', '--skip-patch',
                            default=None,
                            help='Filename pattern to skip')
        parser.add_argument('-S', '--skip-dir',
                            default=None,
                            help='Directory pattern to skip')
        parser.add_argument('DIRECTORY',
                            help='Directory to discover under')
