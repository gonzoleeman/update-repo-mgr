#!/usr/bin/env python3
"""
Database class for update manager
"""

import os
import sys

from update_manager import opts, DEFAULT_DB_DIR, DB_FILE
from update_manager.Util import dprint, vprint

DB_HEADER = '#\n# Database file -- do not edit\n#\n'
DB_HEADER_LEN = len(DB_HEADER)


class Database:
    """
    This class represents the database for the update manager
    """
    def __init__(self, def_db_dir=None):
        self.ur_dir = os.getenv('UR_DIR',os.path.expanduser('~/.ur_dir'))
        self.ensure_ur_dir()
        self.db_file = os.path.join(self.ur_dir, DB_FILE)
        self.ensure_valid_db_file()

    def ensure_ur_dir(self):
        """Create the 'ur' directory, if needed"""
        if not os.path.isdir(self.ur_dir):
            vprint("No DB dir ... creating one (%s) ..." % self.ur_dir)
            try:
                os.mkdir(self.ur_dir)
            except (PermissionError, FileNotFoundError) as err:
                print("oh oh -- mkdir failed:", err, file=sys.stderr)
                sys.exit(1)

    def read_and_validate_db_file(self):
        """Read DB file and validate header is correct"""
        dprint("Reading DB file ...")
        db_file_lines = []
        with open(self.db_file, 'r') as dbf:
            hdr = dbf.read(DB_HEADER_LEN)
            if hdr != DB_HEADER:
                print("oh oh -- database file corrupted: %s" % self.db_file,
                      file=sys.stderr)
                sys.exit(1)
            for e in dbf:
                dprint("Adding line: '%s'" % e.rstrip())
                db_file_lines.append(e.split())
        self.db_file_lines = sorted(db_file_lines, key=lambda e: e[1])
        dprint("post-sort db_file_lines:", self.db_file_lines)

    def ensure_valid_db_file(self):
        if not os.path.isfile(self.db_file):
            dprint("Initializing DB file with header ...")
            with open(self.db_file, 'w') as dbf:
                dbf.write(DB_HEADER)
        else:
            self.read_and_validate_db_file()

    def print_list(self, long=False):
        """Print the list of directories from our database"""
        dprint("Printing DB lines (long=%s)" % long)
        for l in self.db_file_lines:
            if long:
                print('\t'.join(l))
            else:
                print(l[1])

    def entry_present(self, repo_dir):
        """Is this entry already present?"""
        dir_list = [entry[1] for entry in self.db_file_lines]
        dprint("Looking for '%s' in:" % repo_dir, dir_list)
        return repo_dir in dir_list

    def add_to_list(self, repo_dir, repo_type):
        """Add a directory entry to our database"""
        dprint("Adding DB line: '%s\t%s'" % (repo_type, repo_dir))
        self.db_file_lines.append([repo_type, repo_dir])
        self.db_file_lines = sorted(self.db_file_lines, key=lambda e: e[1])
        self.write_out_db_file()

    def write_out_db_file(self):
        """Write out the DB file, so our cache is flushed"""
        dprint("Writing out DB file ...")
        with open(self.db_file, 'w') as dbf:
            dbf.write(DB_HEADER)
            for e in self.db_file_lines:
                dprint("Writing out DB line:", e)
                print('\t'.join(e), file=dbf)
