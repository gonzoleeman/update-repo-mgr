To Test:

* top level

* set DB_DIR to some temp location

- run "ur" -- get help info
- run "ur -h" -- check help info

** test each subcommand

*** list

with no entries

with multiple entries

with wrong options

with no options

with verbose (legal) option

with a repo directory we know should be there

*** add




* or just run:

** ur

* Set up DB directory
  (all subsequent commands use "-D DB_DIR")

* run: "ur -h" (ensure help output)

* run "ur -V" (ensure version output)

* run "ur" (ensure error output)

* run "ur list" (ensure empty list)

* Create a repository of each type?
1. git
2. svn
3. osc

[NOTE: this will be difficult]

* add 3 repos to the list, one at a time, 
ensure "ur list" shows 1, 2, then 3 repos,
and that "ur list -l" shows the repo as well

* remove 3 repos, one at a time, and ensure list shows it

* put 3 back, all at one time

* remove all 3 at one time

* put all 3 back, one at a time

* run "clean" on one of them

* run "clean" on two of them

* run "clean" on all of them (no dir passed in)

* do same for update (like clean)

* test options for clean

* test options for update
