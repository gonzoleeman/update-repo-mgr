#!/usr/bin/python3
"""
Update Repository -- A Tool to make updating a long list of
repositories easier. For Hack Week 2017!

Will handle multiiple repository types.
"""

import sys
import os
from optparse import OptionParser

from update_manager import __version__ as ur_version

from .Opts import Opts, OPTS
from .subcmd import subcmd_in_list, handle_subcmd
from .Database import Database


def parse_args():
    """Parse command-line arguments"""
    parser = OptionParser(version='%prog ' + ur_version,
                          usage=\
                           'Usage: %prog [options] SUBCOMMAND [subcmd_opts]\n' + \
                           '\n' + \
                           'Use "%prog help subcommands" for a list of subcommands',
                          description='For managing repository update and cleaning.')
    parser.disable_interspersed_args()
    parser.add_option('-d', '--debug', action='store_true', default=False,
                      help='enter debug mode')
    parser.add_option('-q', '--quiet', action='store_true', default=False,
                      help='do not produce output')
    (options, arguments) = parser.parse_args()
    OPTS.debug = options.debug
    OPTS.quiet = options.quiet
    if not arguments:
        parser.error("Subcommand required. Use '--help' for details")
        sys.exit(1)
    subcmd = arguments[0]
    subcmd_args = arguments[1:]
    if not subcmd_in_list(subcmd):
        parser.error("Unrecognized subcommand: '%s'." % subcmd)
        sys.exit(1)
    return (parser, subcmd, subcmd_args)


def main():
    """Main entry point"""
    (parser, subcmd, subcmd_args) = parse_args()
    db = Database()
    try:
        res = handle_subcmd(db, parser, subcmd, subcmd_args)
    except KeyboardInterrupt:
        print("\nInterrupted")
        # XXX: clean up?
        return 1
    return res


if __name__ == '__main__':
    main()
