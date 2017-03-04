#!/usr/bin/env python3
"""
Update Repository -- A Tool to make updating a long list of
repositories easier. For Hack Week 2017!

Will handle multiiple repository types.
"""

import sys
import os
from optparse import OptionParser

from update_manager.Util import dprint, vprint
from update_manager import opts
from update_manager.Database import Database
from update_manager.list import handle_list
from update_manager.add import handle_add
from update_manager.rm import handle_rm
from update_manager.update import handle_update

__version__ = '0.1'
__author__ = "Lee Duncan"


subcmd_list = [
    ('help', 'print help information'),
    ('list', 'list managed repositories'),
    ('add', 'add directory to list of repositories'),
    ('rm', 'remove directory from list of repositories'),
    ('update', 'update managed repositories'),
    ]

def subcmd_in_list(subcmd):
    """Is a subcommand in our subcommand list?"""
    return (subcmd in map(lambda x: x[0], subcmd_list))

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
                      dest='debug', help='enter debug mode [False]')
    parser.add_option('-q', '--quiet', action='store_true', default=False,
                      dest='quiet', help='do not produce output [False]')
    parser.add_option('-q', '--verbose', action='store_true', default=False
                      dest='quiet', help='do not be verbose [False]')
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
    if subcmd == 'help':
        if not subcmd_args:
            # treat this like "--help"
            parser.print_help()
            sys.exit(0)
        if subcmd_args[0] != 'subcommands':
            parser.error("Unrecognized help subcommand: '%s'." % \
                         subcmd_args[0])
            sys.exit(1)
        print("Subcommand list:")
        for cmd in subcmd_list:
            print("\t%s\t%s" % (cmd[0], cmd[1]))
        sys.exit(0)
    return (subcmd, subcmd_args)


def main():
    """Main entry point"""
    (subcmd, subcmd_args) = parse_args()
    db = Database()
    dprint("Scanning subcommands ...")
    if subcmd == 'list':
        handle_list(db, subcmd_args)
    elif subcmd == 'add':
        handle_add(db, subcmd_args)
    elif subcmd == 'rm':
        handle_rm(db, subcmd_args)
    elif subcmd == 'update':
        handle_update(db, subcmd_args)
    
    return 0


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
