# Update Repository Manager ur

The `ur` program is a python script that makes dealing with keeping
your repositories up to date much easier.

## Usage

The basic idea is simple: you register your repositories in the
program's database using the `ur add DIRECTORY` command. You then use
`ur update` to update all of the repositories in the database.

## Author

The Author and currently only maintainer:
    Lee Duncan
    lduncan@suse.com

## Dependencies

This package depends on the following python packages:

* python: version 3.11 or higher
* hatch: python-hatch
* hatchling: python-hatchling
* pip: python-pip

## Installation

You can let python3's pip module do the work:

    sh> python3 -mpip install --prefix /usr/local --verbose .

For system-wide installation, you may also wish to set prefix to
"/usr". You may have to be root to install.

You can also install to a "virtual" environment (under your home
directory), using:

    sh> python3 -mpip install --verbose -e .

## Testing

To be filled in

## Code Checking

If you change the code, and wish to submit it, you will need to check
it using "ruff", e.g.:

    sh> ruff check --target-version py313 --preview --config pyproject.toml

