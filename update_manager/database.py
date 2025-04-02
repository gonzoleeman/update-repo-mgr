"""Database class for update manager

We use a file as a "database". There are two columes.

The first column is the "repository type" (e.g. "git",
"osc", or "svn"). The last column is the pathname of
the respository.

It is considered fatal if we need to crete the DB file
and cannot, or if that DB file is corrupted.
"""

import sys
from os import getenv
from pathlib import Path

from .util import dprint, eprint, print_info, wprint

DB_FILE = 'REPO_LIST'
DB_HEADER = '#\n# Database file -- do not edit\n#\n'
DB_HEADER_LEN = len(DB_HEADER)

DB_FILE_COLUMNS = 2

class Database:
    """Represents the database for the update manager"""

    def __init__(self, db_dir: str) -> None:
        """Set up the database class"""
        self.__ur_path = Path(getenv('UR_DIR', db_dir)).expanduser()
        self.ensure_ur_dir()
        self.__db_path = self.__ur_path / DB_FILE
        self.__db_dict: dict[str, str] = {}
        self.ensure_valid_db_file()

    @property
    def db_dict(self) -> dict:
        """Return the database dictionary"""
        return self.__db_dict

    def ensure_ur_dir(self) -> None:
        """Create the 'ur' directory, if needed"""
        if not self.__ur_path.is_dir():
            print_info(f'No DB dir ... creating one ({self.__ur_path}) ...')
            try:
                self.__ur_path.mkdir()
            except (PermissionError, FileNotFoundError) as err:
                eprint(f'mkdir failed: {err}')
                sys.exit(1)

    def read_and_validate_db_file(self) -> None:
        """Read DB file and validate header is correct"""
        dprint(f'Reading DB file ({self.__db_path})')
        with self.__db_path.open(encoding='utf_8') as dbf:
            hdr = dbf.read(DB_HEADER_LEN)
            if hdr != DB_HEADER:
                eprint(f'database file corrupted: {self.__db_path}')
                sys.exit(1)
            for entry in dbf:
                dprint(f'Adding line: "{entry.rstrip()}"')
                entry_split = entry.split()
                if len(entry_split) != DB_FILE_COLUMNS:
                    eprint(f'database file correctuped: {self.__db_path}')
                    dprint(f'line: /{entry}/')
                    sys.exit(1)
                self.db_dict[entry_split[1]] = entry_split[0]
        dprint(f'resulting db_dict: {self.db_dict}')

    def ensure_valid_db_file(self) -> None:
        """Ensure the database isn't corrupt"""
        if not self.__db_path.is_file():
            dprint('Initializing DB file with header ...')
            self.__db_path.write_text(DB_HEADER, encoding='utf_8')
        else:
            self.read_and_validate_db_file()

    def print_list_long(self) -> None:
        """Print the list of repo types and directories from our database"""
        dprint('Printing DB lines: repo-type repo-path')
        for a_key in sorted(self.db_dict):
            a_value = self.db_dict[a_key]
            print(f'{a_value}\t{a_key}')     # noqa: T201

    def print_list_short(self) -> None:
        """Print the list of directories from our database"""
        dprint('Printing DB lines: repo-path')
        for a_key in sorted(self.db_dict):
            print(a_key)                    # noqa: T201

    def entry_present(self, repo_path: Path) -> bool:
        """Is this entry already present?"""
        dprint(f'Looking for "{repo_path}" in dir list')
        return repo_path in self.db_dict

    def add_to_list(self, repo_path: Path, repo_type: str) -> None:
        """Add a directory entry to our database"""
        dprint(f'Adding DB entry: "{repo_type}\t{repo_path}"')
        self.db_dict[str(repo_path)] = repo_type
        self.write_out_db_file()

    def rm_from_list(self, repo_path: Path) -> None:
        """Remove a repo directory from our database"""
        dprint(f'Removing ...DB entry for: {repo_path}')
        del self.db_dict[repo_path]
        self.write_out_db_file()

    def write_out_db_file(self) -> None:
        """Write out the DB file, so our cache is flushed"""
        dprint('Writing out DB file ...')
        with Path(self.__db_path).open(mode='w', encoding='utf_8') as dbf:
            dbf.write(DB_HEADER)
            for k in sorted(self.db_dict):
                a_value = self.db_dict[k]
                a_line = a_value + '\t' + k
                dprint(f'Writing out DB line: /{a_line}/')
                print(a_line, file=dbf)


def skip_dirs_not_in_db(dir_list: list[str], db: Database) -> list[str]:
    """Return dir_list with dirs not in the DB removed"""
    res_dir_list = []
    for a_dir in dir_list:
        if a_dir not in db.db_dict:
            wprint(f'skipping directory not in database: {a_dir}')
        else:
            res_dir_list.append(a_dir)
    return res_dir_list
