"""
The 'clean' subcommand
"""

import sys
from optparse import OptionParser

from .Util import (
    dprint,
    wprint,
    print_multiline_info,
    print_info,
    )
from .repos import update_repo, clean_repo
from .SubCommand import SubCommand
from .Opts import OPTS


class CleanSubCommand(SubCommand):
    def __init__(self, db):
        SubCommand.__init__(self, db, 'clean', 'clean [options]',
                            'Clean up all repositories in the database.')
        dprint("Clean subcommand init routine ...")
        self.parser.add_option('-v', '--verbose', action='store_true',
                               default=False, help='Display more update info')
        self.parser.add_option('-l', '--level', type="int",
                               default=1, help='set cleaning level [Default 1]')
        self.parser.add_option('-s', '--stop-on-error', action='store_true',
                               default=False, help='Stop on update errors')
        self.parser.add_option('-c', '--continue-after-error',
                               action='store_true', default=False,
                               help='Continue a previously-interrupted update')

    def handle_command(self, cmd_args):
        """Handle the 'clean' subcommand"""
        dprint("handling 'clean' args=%s subcommand" % cmd_args)
        (options, arguments) = self.parser.parse_args(cmd_args)
        if len(arguments) != 0:
            self.parser.error("No arguments needed")
            sys.exit(1)
        if options.level < 1:
            self.parser.error("Illegal cleaning level (must be >= 1)")
            sys.exit(1)

        # check for interrupted update in progress
        if options.continue_after_error:
            wprint("'continue' not yet supported -- ignoring")

        # if update-in-progress and not continuing then error exit
        ttl, successes, failures, failure_list = 0, 0, 0, []
        for repo_dir in sorted(self.db.db_dict.keys()):
            ttl = ttl + 1
            repo_type = self.db.db_dict[repo_dir]
            print_info("Cleaning '%s' using '%s'" % (repo_dir, repo_type))
            res = clean_repo(repo_dir, repo_type, options)
            if res:
                failures = failures + 1
                failure_list.append(repo_dir)
            else:
                successes = successes + 1
            if res and options.stop_on_error:
                print_info("Stopping because of error at '%s': %d" %
                           (repo_dir, res))
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
                for f in failure_list:
                    report_arr.append('  ' + f)

            print_multiline_info(report_arr)

        # all done
        subcmd_res = 0
        if failures:
            subcmd_res = 1
        return subcmd_res
