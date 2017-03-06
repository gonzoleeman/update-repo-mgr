#!/usr/bin/env python3
"""
The 'update' subcommand
"""

import sys
from optparse import OptionParser

from update_manager import opts
from update_manager.Util import dprint, print_info, print_multiline_info
from update_manager.repos import update_repo
from update_manager.SubCommand import SubCommand


class UpdateSubCommand(SubCommand):
    def __init__(self, db):
        SubCommand.__init__(self, db, 'update', 'update [options]',
                            'Update all repositories in the database.')
        dprint("Update subcommand init routine ...")
        self.parser.add_option('-v', '--verbose', action='store_true',
                               default=False, help='Display more update info')
        self.parser.add_option('-s', '--stop-on-error', action='store_true',
                               default=False, help='Stop on update errors')
        self.parser.add_option('-c', '--continue-after-error',
                               action='store_true', default=False,
                               help='Continue a previously-interrupted update')

    def handle_command(self, cmd_args):
        """Handle the 'update' subcommand"""
        dprint("handling 'update' args=%s subcommand" % cmd_args)
        (options, arguments) = self.parser.parse_args(cmd_args)
        if len(arguments) != 0:
            self.parser.error("No arguments needed")
            sys.exit(1)

        # check for interrupted update in progress
        if options.continue_after_error:
            print("Warning: 'continue' not yet supported -- ignoring",
                  file=sys.stderr)

        # check for interrupted update in progress
        # if update-in-progress and not continuing then error exit
        ttl, successes, failures, failure_list = 0, 0, 0, []
        for repo_dir in sorted(self.db.db_dict.keys()):
            ttl = ttl + 1
            repo_type = self.db.db_dict[repo_dir]
            print_info("Updating '%s' using '%s'" % (repo_dir, repo_type))
            res = update_repo(repo_dir, repo_type, options)
            dprint("update_repo: returned:", res)
            if res:
                failures = failures + 1
                failure_list.append(repo_dir)
            else:
                successes = successes + 1
            if res and options.stop_on_error:
                print_info("Stopping because of error at '%s'; return=%d" %
                           (repo_dir, res))
                sys.exit(1)
            # mark directory as 'done'

        # remove progress tracking ...

        # print summary report?
        if not opts.quiet:
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
