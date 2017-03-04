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
        self.__db_file = os.path.join(self.ur_dir, DB_FILE)
        self.ensure_valid_db_file()

    @property
    def db_dict(self):
        return self.__db_dict

    def ensure_ur_dir(self):
        """Create the 'ur' directory, if needed"""
        if not os.path.isdir(self.ur_dir):
            vprint("No DB dir ... creating one (%s) ..." % self.ur_dir)
            try:
                os.mkdir(self.ur_dir)
            except (PermissionError, FileNotFoundError) as err:
                print("error: mkdir failed:", err, file=sys.stderr)
                sys.exit(1)

    def read_and_validate_db_file(self):
        """Read DB file and validate header is correct"""
        dprint("Reading DB file ...")
        self.__db_dict = {}
        with open(self.__db_file, 'r') as dbf:
            hdr = dbf.read(DB_HEADER_LEN)
            if hdr != DB_HEADER:
                print("error: database file corrupted: %s" % self.__db_file,
                      file=sys.stderr)
                sys.exit(1)
            for e in dbf:
                dprint("Adding line: '%s'" % e.rstrip())
                i = e.split()
                if len(i) != 2:
                    print("error: database file correctuped: %s" %
                          self.__db_file, file=sys.stderr)
                    print("line: /%s/" % e, file=sys.stderr)
                    sys.exit(1)
                self.__db_dict[i[1]] = i[0]
        dprint("resulting db_dict:", self.__db_dict)

    def ensure_valid_db_file(self):
        if not os.path.isfile(self.__db_file):
            dprint("Initializing DB file with header ...")
            with open(self.__db_file, 'w') as dbf:
                dbf.write(DB_HEADER)
        else:
            self.read_and_validate_db_file()

    def print_list(self, long=False):
        """Print the list of directories from our database"""
        dprint("Printing DB lines (long=%s)" % long)
        for k in sorted(self.__db_dict.keys()):
            if long:
                v = self.__db_dict[k]
                print("%s\t%s" % (v, k))
            else:
                print(k)

    def entry_present(self, repo_dir):
        """Is this entry already present?"""
        dprint("Looking for '%s' in dir list" % repo_dir)
        return self.__db_dict.get(repo_dir, None) is not None

    def add_to_list(self, repo_dir, repo_type):
        """Add a directory entry to our database"""
        dprint("Adding DB entry: '%s\t%s'" % (repo_type, repo_dir))
        self.__db_dict[repo_dir] = repo_type
        self.write_out_db_file()

    def rm_from_list(self, repo_dir):
        """Remove a repo directory from our database"""
        dprint("Removing ...DB entry for: %s" % repo_dir)
        del self.__db_dict[repo_dir]
        self.write_out_db_file()

    def write_out_db_file(self):
        """Write out the DB file, so our cache is flushed"""
        dprint("Writing out DB file ...")
        with open(self.__db_file, 'w') as dbf:
            dbf.write(DB_HEADER)
            for k in sorted(self.__db_dict.keys()):
                v = self.__db_dict[k]
                l = v + '\t' + k
                dprint("Writing out DB line: /%s/" % l)
                print(l, file=dbf)
