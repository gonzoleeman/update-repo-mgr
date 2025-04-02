"""Utility routines for update repository"""

import subprocess
import sys
import typing
from pathlib import Path

from .opts import OPTS


def dprint(*args: str) -> None:
    """Debug printing"""
    if OPTS.debug and args:
        print('DEBUG: ', file=sys.stderr, end='')   # noqa: T201
        for arg in args:
            print(arg, file=sys.stderr, end='')     # noqa: T201
        print(file=sys.stderr)                      # noqa: T201


def eprint(*args: str) -> None:
    """Error printing"""
    if args:
        print('Error: ', file=sys.stderr, end='')   # noqa: T201
        for arg in args:
            print(arg, file=sys.stderr, end='')     # noqa: T201
        print(file=sys.stderr)  # noqa: T201


def wprint(*args: str) -> None:
    """Warning printing"""
    if args:
        print('Warning: ', file=sys.stderr, end='') # noqa: T201
        for arg in args:
            print(arg, file=sys.stderr, end='')     # noqa: T201
        print(file=sys.stderr)                      # noqa: T201


def print_info(*args: str) -> None:
    """Print informational message"""
    if not OPTS.quiet:
        print('***')                                # noqa: T201
        print('*** ', end='')                       # noqa: T201
        for arg in args:
            print(arg + ' ', end='')                # noqa: T201
        print()                                     # noqa: T201
        print('***')                                # noqa: T201


def print_multiline_info(lines: list[str]) -> None:
    """Print an informational message that is more than one line"""
    if not OPTS.quiet:
        print('***')                                # noqa: T201
        for a_line in lines:
            print('*** ' + a_line)                  # noqa: T201
        print('***')                                # noqa: T201


def run_cmd_in_dir(dir_path: Path, cmd_arr: list[str]) -> int:
    """'cd' to 'dir_path', then run command

    Wait for the result
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


def run_cmd_in_dir_ret_output(dir_path: Path, cmd_arr: list[str]) -> (int, typing.TextIO):
    """'cd' to dir_path, then run command

    Wait for result

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
