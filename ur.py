#!/usr/bin/env python3
"""
Update Repository -- A Tool to make updating a long list of
repositories easier. For Hack Week 2017!

Will handle multiiple repository types.
"""

import sys
import os
from optparse import OptionParser

from update_manager.Util import dprint
from update_manager import opts
from update_manager.Database import Database
from update_manager.subcmd import handle_subcmd
from update_manager.subcmd import subcmd_in_list

__version__ = '0.1'
__author__ = "Lee Duncan"


def parse_args():
    """Parse command-line arguments"""
    global opts
    
    parser = OptionParser(version='%prog ' + __version__,
                          usage=\
                           'Usage: %prog [options] SUBCOMMAND\n' + \
                           '\n' + \
                           'Use "%prog help subcommands" for a list of subcommands')
    parser.disable_interspersed_args()
    parser.add_option('-d', '--debug', action='store_true', default=False,
                      help='enter debug mode [False]')
    parser.add_option('-q', '--quiet', action='store_true', default=False,
                      help='do not produce output [False]')
    parser.add_option('-v', '--verbose', action='store_true', default=False,
                      help='do not be verbose [False]')
    (options, arguments) = parser.parse_args()
    opts.debug = options.debug
    opts.quiet = options.quiet
    opts.verbose = options.verbose
    if not arguments:
        parser.error("Subcommand required. Use '--help' for details")
        sys.exit(1)
    subcmd = arguments[0]
    subcmd_args = arguments[1:]
    if not subcmd_in_list(subcmd):
        parser.error("Unrecognized subcommand: '%s'." % subcmd)
        sys.exit(1)
    dprint("Handling subcommand:", subcmd)
    if subcmd == 'help' and not subcmd_args:
        # treat this like "--help"
        parser.print_help()
        sys.exit(0)
    return (parser, subcmd, subcmd_args)


def main():
    """Main entry point"""
    (parser, subcmd, subcmd_args) = parse_args()
    db = Database()
    res = handle_subcmd(db, parser, subcmd, subcmd_args)
    return res


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
