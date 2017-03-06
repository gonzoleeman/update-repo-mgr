#!/usr/bin/env python3
"""
Setup file for installation of the update repo command
"""

import os
import sys
import shutil
import site
from distutils.core import setup, Command


class CleanCommand(Command):
    description = "custom clean command that forcefully removes dist/build directories"
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        print("removing './build', and everything under it")
        os.system('rm -rf ./build')
        print("removing './scripts', and everything under it")
        os.system('rm -rf ./scripts')

shutil.rmtree("scripts", ignore_errors=True)
os.makedirs("scripts")
shutil.copyfile("ur.py", "scripts/ur")

setup(# distribution meta-data
        cmdclass={
            'clean': CleanCommand
            },
        author="Lee Dunan",
        author_email="lduncan@suse.com",
        name="ur",
        packages=["update_manager"],
        scripts=["scripts/ur"],
        version="0.1")
