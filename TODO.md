# List of things to do:

* Add option to add directories to the database from a file (or
  stdin?), to make starting up with lots of pre-existing repos

* Create/fix the "continue" functionality

* Enhancement: add time statistics in report output, e.g. total time,
  average time per repository (perhaps by type?)

* Track actions that are skipped, like "clean" for non-git repos,
  and show "repos skipped" during the report

* BUG: "ur list" with no DB file fails?

* add in static type checking (mypy) and pylint
  - how to do this automatically?

* add in use of linting too (use "ruff"?)

* add in ability to scan for repo directories

* fix bug where default directory is hard-coded, even though there
  is a default value
  
* add ability to specify type of repo (e.g. "git", etc), for
  operations where appropriate (like list, update, clean)

* show better progress info: at least the repo count?
  (e.g. at least repo number, or "N of M"?)

* store/retrieve DB file as a single data struct.
  - would require creating a data structure/class for the data

* create a man page?

* make subcommand gathering/usage automatic, i.e. any method in some
  sub-directory, or matching a name pattern?

* add selt-tests! -- pyunit is ok for unit testing, but we also
  need command-level testing

  Looking at: pytest, pytest-cov

  What about: pyunit?

* Handle "exceptions" better -- right now, in many (all?) cases,
  error handling is done like C: do an exit, or return a failure,
  but never create an exception, because those are ugly

  But that's not pythonic

* Test 'quiet' option -- not sure it does anything

* Find a better way to pass short help and long help (remove them?)

* add subcommand uses absolute path, but other subcommands don't?

* make "short help" vs "long help" (e.g. use "-l"?)

* make "clean" method in repo classes optional
perhaps define class method as static? somehow there needs to be
a default method, if the sub-class does't define it, that does nothing

* document the two (?) environment variables support (man page?)

* use a real/better "database"? (or read/write binary data struct?)
