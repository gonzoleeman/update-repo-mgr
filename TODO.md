# List of things to do:

## Add option to add directories to the database from a file

or stdin? to make starting up with lots of pre-existing repos

might not be needed, since we can pass multiple directories in
on the command line now

## Create/fix the "continue" functionality

it's a good idea, but never implemented

how to you keep track of where you "stopped"?

right now, I believe on update can fail? But whatever can fail
should leave a marker some place, so it can be continued later

but what if the DB has changed since the marker?

## Enhancement: add time statistics in report output, e.g. total time,

  average time per repository (perhaps by type?)

  total time

## Track actions that are skipped, like "clean" for non-git repos

  and show "repos skipped" during the report

## BUG: "ur list" with no DB file fails?

I believe it causes an exception?

## add in ability to scan for repo directories

## add ability to specify type of repo (e.g. "git", etc), for
  operations where appropriate (like list, update, clean)

## show better progress info: at least the repo count?
  (e.g. at least repo number, or "N of M"?)

## store/retrieve DB file as a single data struct.
  - would require creating a data structure/class for the data

## create a man page?

## make subcommand gathering/usage automatic, i.e. any method in some
  sub-directory, or matching a name pattern?

## add selt-tests! -- pyunit is ok for unit testing, but we also
  need command-level testing

  Looking at: pytest, pytest-cov

  What about: pyunit?

## Handle "exceptions" better -- right now, in many (all?) cases,
  error handling is done like C: do an exit, or return a failure,
  but never create an exception, because those are ugly

  But that's not pythonic

## Test 'quiet' option -- not sure it does anything

## make "short help" vs "long help" (e.g. use "-l"?)

## make "clean" method in repo classes optional
perhaps define class method as static? somehow there needs to be
a default method, if the sub-class does't define it, that does nothing

## document the two (?) environment variables support (man page?)

## use a real/better "database"? (or read/write binary data struct?)

## combine subcmd.py and sub_command.py

names for modules are confusing, in general

there's also repo.py and repos.py :(

maybe subdirectory(s) should be use, e.g. for "repos", and for
"subcommands"??

## use "logging" instead of dprint/eprint/wprint

not sure if I could also use this to print to stdout, i.e. still might
need "print()" for the "list" command

## command line options for "ur clean"

the "level" option should be limited to [1, 2, 3]

## the "ur clean" report should include the "level"

## create common "report" function

for update and clean to use, since they have almost identical code
