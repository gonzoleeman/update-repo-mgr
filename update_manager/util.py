"""
Utility routines for update repository
"""

import sys
import subprocess

from .opts import OPTS


def dprint(*args):
    """Debug printing"""
    if OPTS.debug and args:
        print('DEBUG: ', file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print(file=sys.stderr)


def eprint(*args):
    """Error printing"""
    if args:
        print('Error: ', file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print(file=sys.stderr)


def wprint(*args):
    """Warning printing"""
    if args:
        print('Warning: ', file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print(file=sys.stderr)


def print_info(*args):
    """Print informational message"""
    if not OPTS.quiet:
        print('***')
        print('*** ', end='')
        for arg in args:
            print(arg + ' ', end='')
        print()
        print('***')


def print_multiline_info(lines):
    """Print an informational message that is more than one line"""
    if not OPTS.quiet:
        print('***')
        for a_line in lines:
            print('*** ' + a_line)
        print('***')


def run_cmd_in_dir(dir_path, cmd_arr):
    """
    'cd' to dir_path, then run supplied command, waiting for result
    """
    cmd_str = ' '.join(cmd_arr)
    dprint(f'Running (dir={dir_path}) cmd: "{cmd_str}"')
    my_proc = subprocess.Popen(cmd_arr, cwd=dir_path)
    my_proc.communicate()
    wstat = my_proc.returncode
    if wstat != 0:
        dprint(f'error: ret_stat={wstat}')
        print_info(f'warning: "{cmd_str}" in {dir_path} failed')
    return wstat


def run_cmd_in_dir_ret_output(dir_path, cmd_arr):
    """
    'cd' to dir_path, then run supplied command, waiting for result

    Also, the output will not be displayed but instead will be
    returned to the caller together with the exit status
    """
    cmd_str = ' '.join(cmd_arr)
    dprint(f'Running [save output] (dir={dir_path}) cmd: "{cmd_str}"')
    my_proc = subprocess.Popen(cmd_arr, cwd=dir_path, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    (std_output, err_output) = my_proc.communicate()
    if std_output:
        dprint(f'std_output: {std_output}')
    if err_output:
        dprint(f'err_output: {err_output}')
    wstat = my_proc.returncode
    dprint(f'wstat= {wstat}')
    if wstat != 0:
        dprint(f'error: ret_stat= {wstat}')
        print_info(f'warning: "{cmd_str}" in {dir_path} failed')
    return (wstat, std_output)
