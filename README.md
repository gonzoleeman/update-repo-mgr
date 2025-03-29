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

## Installation

You can let python3's pip module do the work:

    sh> python3 -mpip install --prefix /usr/local --verbose .

Note that you will have to be root to install to prefix "/usr".
