"""
Utility routines for update repository
"""

from __future__ import print_function

import os
import sys
import subprocess

from update_manager import opts



def dprint(*args):
    """Debug printing"""
    if opts.debug and args:
        print("DEBUG: ", file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print('', file=sys.stderr)

def eprint(*args):
    """Error printing"""
    if args:
        print("Error: ", file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print('', file=sys.stderr)

def wprint(*args):
    """Warning printing"""
    if args:
        print("Warning: ", file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print('', file=sys.stderr)

def print_info(*args):
    if not opts.quiet:
        print('***')
        print('*** ', end='')
        for arg in args:
            print(arg + ' ', end='')
        print()
        print('***')

def print_multiline_info(lines):
    if not opts.quiet:
        print('***')
        for l in lines:
            print('*** ' + l)
        print('***')

def run_cmd_in_dir(dir_path, cmd_arr):
    """
    'cd' to dir_path, then run supplied command, waiting for result
    """
    dprint("Running (dir=%s) cmd: \"%s\"" % (dir_path, ' '.join(cmd_arr)))
    p = subprocess.Popen(cmd_arr, cwd=dir_path)
    p.communicate()
    wstat = p.returncode
    if wstat != 0:
        dprint("error: ret_stat=", wstat)
        print_info('warning: "%s" in %s failed' % (' '.join(cmd_arr), dir_path))
    return wstat

def run_cmd_in_dir_ret_output(dir_path, cmd_arr):
    """
    'cd' to dir_path, then run supplied command, waiting for result

    Also, the output will not be displayed but instead will be
    returned to the caller together with the exit status
    """
    dprint("Running [save output] (dir=%s) cmd: \"%s\"" %
           (dir_path, ' '.join(cmd_arr)))
    p = subprocess.Popen(cmd_arr, cwd=dir_path, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    (std_output, err_output) = p.communicate()
    if std_output:
        dprint("std_output:", std_output)
    if err_output:
        dprint("err_output:", err_output)
    wstat = p.returncode
    dprint("wstat=", wstat)
    if wstat != 0:
        dprint("error: ret_stat=", wstat)
        print_info('warning: "%s" in %s failed' % (' '.join(cmd_arr), dir_path))
    return (wstat, std_output)

