"""The 'clean' subcommand"""

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from .database import Database, skip_dirs_not_in_db
from .repos import clean_repo
from .sub_command import SubCommand
from .util import dprint, print_info, print_multiline_info


class CleanSubCommand(SubCommand):
    """Clean one or more repository directories"""

    def __init__(self, database: Database, parser: ArgumentParser, args: Namespace) -> None:
        """Initialize clean subcommand."""
        SubCommand.__init__(self, database, parser, args)
        dprint(f'"clean" subcommand init routine, args={args}')

    def handle_command(self) -> int:
        """Handle the 'clean' subcommand"""
        # TODO(lee): we ignore errors in 'clean'?
        dir_list = self.args.DIRECTORY
        dprint(f'handle_command("clean", dir_list={dir_list}) called')
        if dir_list:
            # validate directories
            dir_list = skip_dirs_not_in_db(dir_list, self.database)
            dprint(f'updated dir_list: {dir_list}')

        ttl, successes, failure_list = 0, 0, []
        for a_dir in sorted(self.database.db_dict):

            if dir_list and a_dir not in dir_list:
                dprint(f'skipping directory: {a_dir}')
                continue

            ttl += 1
            repo_type = self.database.db_dict[a_dir]
            # TODO(lee): should we check dir still present
            print_info(f'"Cleaning "{a_dir}" using "{repo_type}"')
            res = clean_repo(Path(a_dir).resolve(), repo_type, self.args)
            dprint(f'clean_repo: returned: {res}')
            if res:
                failure_list.append(a_dir)
            else:
                successes += 1
            if res and self.args.stop_on_error:
                print_info(f'Stopping because of error at "{a_dir}": {res}')
                sys.exit(1)
            # mark directory as 'done'

        # print summary report?
        failures = len(failure_list)
        if not self.args.quiet:
            report_arr = [
                '"Clean" Summary Report',
                '',
                f'Directories Cleaned: {ttl:3d}',
                f'Successes:           {successes:3d}',
                f'Failures:            {failures:3d}',
                ]

            if failures:
                report_arr = [*report_arr, '', 'Failure List:']
                for failure in failure_list:
                    report_arr.append('  ' + failure)

            print_multiline_info(report_arr)

        # all done
        return 1 if failures else 0

    @classmethod
    def add_options(cls, parser: ArgumentParser) -> None:
        """Add options for the "clean" subcommand"""
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            default=False,
                            help='Clean verbosely')
        parser.add_argument('-s', '--stop-on-error',
                            action='store_true',
                            default=False,
                            help='Stop cleaning on error')
        parser.add_argument('-l', '--level',
                            type=int,
                            default=1,
                            help='Set cleaning level [Default 1]')
        parser.add_argument('DIRECTORY',
                            nargs='*',
                            help='Directory to clean')
