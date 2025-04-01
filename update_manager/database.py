"""
Database class for update manager
"""

import os
import sys

from .util import dprint, eprint, print_info

DB_FILE = 'REPO_LIST'
DB_HEADER = '#\n# Database file -- do not edit\n#\n'
DB_HEADER_LEN = len(DB_HEADER)


class Database:
    """
    This class represents the database for the update manager
    """
    def __init__(self):
        self.ur_dir = os.getenv('UR_DIR', os.path.expanduser('~/.ur_dir'))
        self.ensure_ur_dir()
        self.__db_file = os.path.join(self.ur_dir, DB_FILE)
        self.__db_dict = {}
        self.ensure_valid_db_file()

    @property
    def db_dict(self):
        """return the database dictionary"""
        return self.__db_dict

    def ensure_ur_dir(self):
        """Create the 'ur' directory, if needed"""
        if not os.path.isdir(self.ur_dir):
            print_info(f'No DB dir ... creating one ({self.ur_dir}) ...')
            try:
                os.mkdir(self.ur_dir)
            except (PermissionError, FileNotFoundError) as err:
                eprint(f'mkdir failed: {err}')
                sys.exit(1)

    def read_and_validate_db_file(self):
        """Read DB file and validate header is correct"""
        dprint(f'Reading DB file ({self.__db_file})')
        with open(self.__db_file, 'r') as dbf:
            hdr = dbf.read(DB_HEADER_LEN)
            if hdr != DB_HEADER:
                eprint(f'database file corrupted: {self.__db_file}')
                sys.exit(1)
            for entry in dbf:
                dprint(f'Adding line: "{entry.rstrip()}"')
                entry_split = entry.split()
                if len(entry_split) != 2:
                    eprint(f'database file correctuped: {self.__db_file}')
                    print(f'line: /{entry}/', file=sys.stderr)
                    sys.exit(1)
                self.__db_dict[entry_split[1]] = entry_split[0]
        dprint(f'resulting db_dict: {self.__db_dict}')

    def ensure_valid_db_file(self):
        """Ensure the database isn't corrupt"""
        if not os.path.isfile(self.__db_file):
            dprint('Initializing DB file with header ...')
            with open(self.__db_file, 'w') as dbf:
                dbf.write(DB_HEADER)
        else:
            self.read_and_validate_db_file()

    def print_list(self, long=False):
        """Print the list of directories from our database"""
        dprint(f'Printing DB lines (long={long})')
        for a_key in sorted(self.__db_dict):
            if long:
                a_value = self.__db_dict[a_key]
                print(f'{a_value}\t{a_key}')
            else:
                print(a_key)

    def entry_present(self, repo_dir):
        """Is this entry already present?"""
        dprint(f'Looking for "{repo_dir}" in dir list')
        return self.__db_dict.get(repo_dir, None) is not None

    def add_to_list(self, repo_dir, repo_type):
        """Add a directory entry to our database"""
        dprint(f'Adding DB entry: "{repo_type}\t{repo_dir}"')
        self.__db_dict[repo_dir] = repo_type
        self.write_out_db_file()

    def rm_from_list(self, repo_dir):
        """Remove a repo directory from our database"""
        dprint(f'Removing ...DB entry for: {repo_dir}')
        del self.__db_dict[repo_dir]
        self.write_out_db_file()

    def write_out_db_file(self):
        """Write out the DB file, so our cache is flushed"""
        dprint('Writing out DB file ...')
        with open(self.__db_file, 'w') as dbf:
            dbf.write(DB_HEADER)
            for k in sorted(self.__db_dict.keys()):
                a_value = self.__db_dict[k]
                a_line = a_value + '\t' + k
                dprint(f'Writing out DB line: /{a_line}/')
                print(a_line, file=dbf)
