"""Utility routines for update repository"""

import subprocess
import sys
from pathlib import Path

from .opts import OPTS


def dprint(*args: str) -> None:
    """Debug printing"""
    if OPTS.debug and args:
        print('DEBUG: ', file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print(file=sys.stderr)


def eprint(*args: str) -> None:
    """Error printing"""
    if args:
        print('Error: ', file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print(file=sys.stderr)


def wprint(*args: str) -> None:
    """Warning printing"""
    if args:
        print('Warning: ', file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print(file=sys.stderr)


def print_info(*args: str) -> None:
    """Print informational message"""
    if not OPTS.quiet:
        print('***')
        print('*** ', end='')
        for arg in args:
            print(arg + ' ', end='')
        print()
        print('***')


def print_multiline_info(lines: list[str]) -> None:
    """Print an informational message that is more than one line"""
    if not OPTS.quiet:
        print('***')
        for a_line in lines:
            print('*** ' + a_line)
        print('***')


def run_command(command: str, cwd: Path | None = None):
    """Run a command, with optional input and output supplied."""
    ret = subprocess.run(command.split(), encoding='utf-8',
                         capture_output=True, shell=False,
                         check=False, cwd=cwd)
    if ret.returncode != 0:
        dprint(f'error: ret_stat={ret.returncode}')
        print_info(f'warning: "{command}" in {cwd} failed')
    return ret
