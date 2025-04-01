"""The 'update' subcommand"""

import sys

from .util import (
    dprint,
    eprint,
    print_multiline_info,
    print_info,
    )
from .repos import update_repo
from .sub_command import SubCommand


class UpdateSubCommand(SubCommand):
    """
    Update one or more repo directories
    """
    def __init__(self, database, parser, args):
        SubCommand.__init__(self, database, parser, args)
        dprint(f'"update" subcommand init routine, args={args}')

    def handle_command(self, short_help=None, long_help=None):
        dprint(f'handle_command("update", "{short_help}", "{long_help}")')

        dir_list = self.args.DIRECTORY
        dprint(f'update: directories: {dir_list}')
        if dir_list:
            # ensure dir list passed in contains valid directories in the DB
            for a_dir in dir_list:
                if a_dir not in self.database.db_dict:
                    eprint(f'specified directory not in list: {a_dir}')
                    sys.exit(1)

        dprint(f'update dir_list: {dir_list}')

        # try to update each repo, keeing count
        ttl, successes, failures, failure_list = 0, 0, 0, []
        for a_dir in sorted(self.database.db_dict):

            if dir_list and a_dir not in dir_list:
                dprint(f'skipping directory: {a_dir}')
                continue

            ttl += 1

            repo_type = self.database.db_dict[a_dir]

            print_info(f'Updating "{a_dir}" using "{repo_type}"')

            res = update_repo(a_dir, repo_type, self.args)
            dprint(f'update_repo: returned: {res}')

            if res:
                failures += 1
                failure_list.append(a_dir)
            else:
                successes += 1

            if res and self.args.stop_on_error:
                print_info(
                    f'Stopping because of error at "{a_dir}"; return={res}')
                sys.exit(1)

            # XXX: mark directory as 'done'

        # remove progress tracking (XXX: huh?)

        # print summary report?
        if not self.args.quiet:
            report_arr = [
                '"Update" Summary Report',
                '',
                f'Directories Updated: {ttl:3d}',
                f'Successes:           {successes:3d}',
                f'Failures:            {failures:3d}',
                ]

            if failures:
                report_arr = [*report_arr, '', 'Failure List:']
                for failure in failure_list:
                    report_arr.append('  ' + failure)

            print_multiline_info(report_arr)

        # all done
        subcmd_res = 0
        if failures:
            subcmd_res = 1
        return subcmd_res

    @classmethod
    def add_options(cls, parser):
        """Add options for the "update" subcommand"""
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            default=False,
                            help='Update verbosely')
        parser.add_argument('-s', '--stop-on-error',
                            action='store_true',
                            default=False,
                            help='Stop updating on error')
        parser.add_argument('DIRECTORY',
                            nargs='*',
                            help='Directory to update')
