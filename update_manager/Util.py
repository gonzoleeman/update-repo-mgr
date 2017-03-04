#!/usr/bin/env python3
"""
Utility routines for update repository
"""

import os
import sys
from update_manager import opts



def dprint(*args):
    """Debug printing"""
    if opts.debug and args:
        print("DEBUG: ", file=sys.stderr, end='')
        for arg in args:
            print(arg, file=sys.stderr, end='')
        print('', file=sys.stderr)

def vprint(*args):
    if opts.quiet:
        return
    print('***')
    print('*** ', end='')
    for arg in args:
        print(arg + ' ', end='')
    print()
    print('***')

def run_cmd_in_dir(dir_path, cmd_arr):
    """'cd' to dir_path, then run supplied command, waiting for result"""
    dprint("Running (dir=%s) cmd: %s" % (dir_path, ' '.join(cmd_arr)))
    pid = os.fork()
    if pid < 0:
        print("Error: cannot fork!\n", file=sys.stderr)
        sys.exit(1)
    if pid == 0:
        # the child
        dprint("Child changing to directory: %s" % dir_path)
        os.chdir(dir_path)
        dprint("Child running cmd: %s, args:" % cmd_arr[0], cmd_arr)
        os.execvp(cmd_arr[0], cmd_arr)
        # not reached
    if pid > 0:
        # the parent
        wpid, wstat = os.waitpid(pid, 0)
        if wstat != 0:
            dprint("error: ret_stat=", wstat)
        return wstat

