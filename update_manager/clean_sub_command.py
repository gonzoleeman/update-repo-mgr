"""
The 'clean' subcommand
"""

import sys

from .util import (
    dprint,
    eprint,
    print_multiline_info,
    print_info,
    )
from .repos import clean_repo
from .sub_command import SubCommand
from .opts import OPTS


class CleanSubCommand(SubCommand):
    """
    Clean one or more repository directories
    """
    def __init__(self, database, parser, args):
        SubCommand.__init__(self, database, parser, args)
        dprint(f'"clean" subcommand init routine, args={args}')

    def handle_command(self, short_help=None, long_help=None):
        """Handle the 'clean' subcommand"""
        dprint('handling "clean" subcommand')

        dprint(f'clean: directories: {self.args.DIRECTORY}')

        directory_list = self.args.DIRECTORY
        if directory_list:
            # validate directories
            for a_dir in directory_list:
                if not a_dir in self.database.db_dict:
                    eprint(f'specified directory not in list: {a_dir}')
                    sys.exit(1)

        dprint(f'update directory_list: {directory_list}')

        # if update-in-progress and not continuing then error exit
        ttl, successes, failures, failure_list = 0, 0, 0, []
        for a_dir in sorted(self.database.db_dict.keys()):

            if directory_list and a_dir not in directory_list:
                dprint(f'skipping directory: {a_dir}')
                continue

            ttl = ttl + 1
            repo_type = self.database.db_dict[a_dir]
            print_info(f'"Cleaning "{a_dir}" using "{repo_type}"')
            res = clean_repo(a_dir, repo_type, self.args)
            if res:
                failures = failures + 1
                failure_list.append(a_dir)
            else:
                successes = successes + 1
            if res and self.args.stop_on_error:
                print_info(f'Stopping because of error at "{a_dir}": {res}')
                sys.exit(1)
            # mark directory as 'done'

        # remove progress tracking ...

        # print summary report?
        if not OPTS.quiet:
            report_arr = [
                '"Clean" Summary Report',
                '',
                'Directories Cleaned: %3d' % ttl,
                'Successes:           %3d' % successes,
                'Failures:            %3d' % failures]

            if failures:
                report_arr = report_arr + ['', 'Failure List:']
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
