# List of things to do:

* Add option to add directories to the database from a file (or
  stdin?), to make starting up with lots of pre-existing repos

* Still need to plumb the "continue" functionality, but first must
  decide the functionality desired. Do we want to "grey list" some
  directories, e.g. if they aren't updating right now but we want to
  leave them in the database? How about having an "enable" bit for
  each directory (like zypper does for repositories)? Maybe the
  "update" subcommand should (in interactive mode at least) ask the
  caller if they want to skip, ignore, or continue when an update
  doesn't work (again, like zypper)?

* Enhancement: add option to the `update` subcommand to be able to
  pass in a single directory and have just it updated. Could this be
  useful for more than one? (Not sure how)

* Enhancement: add time statistics in report output, e.g. total time,
  average time per repository (perhaps by type?)

* Track actions that are skipped, like "clean" for non-git repos,
  and show "repos skipped" during the report

* Bug: "ur list" on very first use fails with stack dump. Next run
  succeeds.
