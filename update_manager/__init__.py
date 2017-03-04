#!/usr/bin/env python3
"""
Update Manager library
"""

import os
from update_manager.Opts import Opts

__version__ = '1.1'
__author__ = 'Lee Duncan'

__all__ = [
    'Util',
    ]


DEFAULT_DB_DIR = '~/.ur_dir'
DB_FILE = 'REPO_LIST'


class Opts:
    """Global option class"""
    pass


opts = Opts()
