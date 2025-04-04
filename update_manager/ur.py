"""Update Repository

This is the update repository tool. A Tool to make
updating a long list of repositories easier. For Hack Week 2017!

Will handle multiiple repository types.
"""

from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter

from update_manager import __version__ as ur_version

from .database import Database
from .opts import OPTS
from .subcmd import SUBCMD_DICT, handle_subcmd
from .util import dprint


def reformat_subcmd_help(msg: str) -> str:
    """Reformat subcommand help message

    Reformat message of the form:

    > usage: ur SUBCMD ...
    > ... (more lines)

    by: * replacing "^usage: " with "> "
        * indenting all lines 4 spaces
        * adding a blank line at the end
    """
    lines = msg.splitlines()
    return_lines = []
    for line in lines:
        line_copy = line
        if line_copy.startswith('usage: '):
            line_copy = 'sh> ' + line_copy[len('usage: '):]
        line_copy = 4 * ' ' + line_copy
        return_lines += [line_copy]
    return_lines += ['', '']
    return '\n'.join(return_lines)


def define_parser() -> ArgumentParser:
    """Set up parser with subparsers"""
    parent_parser = ArgumentParser(
        description='For managing repository update and cleaning.',
        formatter_class=RawDescriptionHelpFormatter)

    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'%(prog)s {ur_version}',
        help='print version information and exit')
    parent_parser.add_argument(
        '-d', '--debug',
        action='store_true',
        default=False,
        help='enter debug mode')
    parent_parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=False,
        help='do not produce output')
    parent_parser.add_argument(
        '-D', '--db-directory',
        nargs=1,
        type=str,
        default=OPTS.db_dir,
        help=f'override default DB directory ({OPTS.db_dir}))')

    subparsers = parent_parser.add_subparsers(dest='subcommand')
    subcmd_help = ['subcommand usage:\n', '\n']
    for subcmd_name in SUBCMD_DICT:
        sub_parser = subparsers.add_parser(
            subcmd_name,
            add_help=False,
            description=SUBCMD_DICT[subcmd_name].__doc__,
            help=SUBCMD_DICT[subcmd_name].__doc__)
        # call class method to set up arguments for this class
        subcmd_class = SUBCMD_DICT[subcmd_name]
        subcmd_class.add_options(sub_parser)

        # set up subcommand usage
        subcmd_msg = sub_parser.format_help()
        subcmd_help += [reformat_subcmd_help(subcmd_msg)]

        #
        # this is the shorter version of subcommand help ....
        #
        # subcmd_msg = sub_parser.format_usage().split()
        # if subcmd_msg[0] == 'usage:':
        #     subcmd_msg = subcmd_msg[1:]
        # subcmd_help += [4 * ' ' + ' '.join(subcmd_msg)]
        #

    parent_parser.epilog = ''.join(subcmd_help)

    return parent_parser


def parse_args() -> tuple[ArgumentParser, Namespace]:
    """Parse command-line arguments"""
    parser = define_parser()
    args = parser.parse_args()
    if args.subcommand is None:
        parser.error('must supply subcommand. Use "ur -h" for help')
    OPTS.debug = args.debug
    OPTS.quiet = args.quiet
    OPTS.db_dir = args.db_directory
    dprint(f'args: {args}')
    return (parser, args)


def main() -> int:
    """Let's update us some repositories!"""
    (parser, args) = parse_args()
    database = Database(OPTS.db_dir)
    try:
        res = handle_subcmd(database, parser, args)
    except KeyboardInterrupt:
        print('\nInterrupted')      # noqa: T201
        return 1
    return res


if __name__ == '__main__':
    main()
