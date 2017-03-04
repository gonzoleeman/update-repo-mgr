#!/usr/bin/env python3
"""
The 'list' subcommand
"""

from optparse import OptionParser

from update_manager.Util import dprint


def handle_list(db, list_args):
    """Handle the 'list' subcommand"""
    dprint("handling 'list' args=%s subcommand" % list_args)
    parser = OptionParser(usage='Usage: %prog [program_options] list [options]')
    parser.add_option('-l', '--long', action='store_true', default=False)
    (options, arguments) = parser.parse_args(list_args)
    db.print_list(long=options.long)

