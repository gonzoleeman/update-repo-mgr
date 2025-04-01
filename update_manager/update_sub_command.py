"""
The 'update' subcommand
"""

import sys

from .util import (
    dprint,
    wprint,
    eprint,
    print_multiline_info,
    print_info,
    )
from .repos import update_repo
from .sub_command import SubCommand
from .opts import OPTS


class UpdateSubCommand(SubCommand):
    """
    Update one or more repo directories
    """
    def __init__(self, db, parser, args):
        SubCommand.__init__(self, db, parser, args)
        dprint('"update" subcommand init routine, args={args}')

    def handle_command(self):
        dprint('handling "update" subcommand')

        # XXX
        # check for "continue on error" ???

        # XXX
        # check for interrupted update in progress
        # if update-in-progress and not continuing then error exit

        dprint(f'update: directories: {self.args.DIRECTORY}')
        directory_list = self.args.DIRECTORY
        if directory_list:
            # validate directories
            for a_dir in directory_list:
                if not a_dir in self.db.db_dict:
                    eprint(f'specified directory not in list: {a_dir}')
                    sys.exit(1)

        dprint(f'update directory_list: {directory_list}')
        
        # try to update each repo, keeing count
        ttl, successes, failures, failure_list = 0, 0, 0, []
        for repo_dir in sorted(self.db.db_dict):

            if directory_list and repo_dir not in directory_list:
                dprint(f'skipping directory: {repo_dir}')
                continue

            ttl += 1

            repo_type = self.db.db_dict[repo_dir]

            print_info(f'Updating "{repo_dir}" using "{repo_type}"')

            res = update_repo(repo_dir, repo_type, self.args)
            dprint(f'update_repo: returned: {res}')

            if res:
                failures += 1
                failure_list.append(repo_dir)
            else:
                successes += 1

            if res and options.stop_on_error:
                print_info(
                    f'Stopping because of error at "{repo_dir}"; return={res}')
                sys.exit(1)

            # XXX: mark directory as 'done'

        # remove progress tracking (XXX: huh?)

        # print summary report?
        if not OPTS.quiet:
            report_arr = [
                '"Update" Summary Report',
                '',
                'Directories Updated: %3d' % ttl,
                'Successes:           %3d' % successes,
                'Failures:            %3d' % failures]

            if failures:
                report_arr = report_arr + ['', 'Failure List:']
                for f in failure_list:
                    report_arr.append('  ' + f)

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
