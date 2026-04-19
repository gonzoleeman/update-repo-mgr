"""Update Manager options.

Copyright 2026, Lee Duncan, All Rights Reserved.
"""

from dataclasses import dataclass


@dataclass
class Opts:
    """Global Options class."""

    debug: bool = False
    quiet: bool = False
    db_dir: str = '~/.ur_dir'


OPTS = Opts()
