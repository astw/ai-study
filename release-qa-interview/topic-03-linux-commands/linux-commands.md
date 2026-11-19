# Linux Commands for Release QA

A practical Linux command-line guide for a junior-to-mid release QA interview.
Linux examples include the macOS equivalent beside them.

## Contents

- [Part 1 — Orientation and System Information](#part-1--orientation-and-system-information)
- [Part 2 — Files and Folders](#part-2--files-and-folders)
- [Part 3 — Viewing and Searching Text and Logs](#part-3--viewing-and-searching-text-and-logs)
- [Part 4 — Processes and Services](#part-4--processes-and-services)
- [Part 5 — Permissions and Ownership](#part-5--permissions-and-ownership)
- [Part 6 — Disks, Memory, and Archives](#part-6--disks-memory-and-archives)
- [Part 7 — Pipes, Redirection, Exit Codes, and Environment](#part-7--pipes-redirection-exit-codes-and-environment)
- [Part 8 — SSH and File Transfer](#part-8--ssh-and-file-transfer)
- [Part 9 — curl and Network Checks](#part-9--curl-and-network-checks)
- [Part 10 — Release QA Workflows](#part-10--release-qa-workflows)
- [macOS Quick Reference](#macos-quick-reference)

## How to read an entry

Commands carry one of three frequency badges:

- **Day-to-day** — know it cold; you will use it most weeks.
- **Frequent** — use it with a quick reference nearby.
- **Situational** — know it exists and look it up when needed.

Each entry has a flags table, Linux examples, a `**macOS:**` line, one
release-QA use, and a `**Watch out**` line for a common failure.

## Part 1 — Orientation and System Information

### `pwd`

**Day-to-day.** Print the current working directory.

| Flag | What it does |
|---|---|
| `-P` | Show the physical path, resolving symlinks |
| `-L` | Show the logical path (the default) |

**Linux:**

```bash
pwd
pwd -P
```

**macOS:** Same commands.

**Release QA use:** Confirm which build directory a command will run in before
packaging artifacts.

**Watch out:** `pwd` shows the shell's directory, not the directory of a script
you just ran.

### `ls`

**Day-to-day.** List directory contents.

| Flag | What it does |
|---|---|
| `-l` | Long format: permissions, owner, size, time |
| `-a` | Include hidden dotfiles |
| `-h` | Human-readable sizes |
| `-t` | Sort by modification time |

**Linux:**

```bash
ls -lah /var/log/myapp
ls -lt releases
```

**macOS:** Same commands; for color use `ls -G`, because `ls --color` is GNU.

**Release QA use:** Check artifact names, sizes, timestamps, and hidden
configuration files before a release.

**Watch out:** `ls` alone hides dotfiles; use `-a` when checking configuration.

### `cd`

**Day-to-day.** Change the working directory.

| Usage | What it does |
|---|---|
| `cd /path` | Go to an absolute path |
| `cd ..` | Go up one directory |
| `cd ~` | Go to your home directory |
| `cd -` | Go back to the previous directory |

**Linux:**

```bash
cd releases/2026-11-18
cd ..
pwd
```

**macOS:** Same commands.

**Release QA use:** Move between the build output, the artifact directory, and
the log directory.

**Watch out:** A failed `cd` leaves you in the old directory; run `pwd` after a
path you are unsure about.

### `whoami`

**Day-to-day.** Print the current username.

| Usage | What it does |
|---|---|
| `whoami` | Print the effective username |

**Linux:**

```bash
whoami
```

**macOS:** Same command.

**Release QA use:** Confirm which user owns a test process or a file before
changing permissions.

**Watch out:** Under `sudo`, `whoami` prints `root`, not your login user; `id`
or `logname` shows the original account.

### `id`

**Frequent.** Print the user ID, group ID, and group memberships.

| Flag | What it does |
|---|---|
| `-u` | Print only the user ID |
| `-g` | Print only the primary group ID |
| `-G` | Print all group IDs |

**Linux:**

```bash
id
id -u
id -G
```

**macOS:** Same commands.

**Release QA use:** Check whether the test user can read a log or write to an
artifact directory.

**Watch out:** Group membership changes need a new login session before they
appear.

### `uname`

**Frequent.** Print system and kernel information.

| Flag | What it does |
|---|---|
| `-a` | Print everything |
| `-r` | Print the kernel release |
| `-m` | Print the machine hardware name |

**Linux:**

```bash
uname -a
uname -r
```

**macOS:** Same commands.

**Release QA use:** Record the OS and kernel version in a bug report or test
summary.

**Watch out:** `uname` does not identify the Linux distribution; use
`cat /etc/os-release` for that.

### `hostname`

**Frequent.** Print the host name.

| Usage | What it does |
|---|---|
| `hostname` | Print the short host name |
| `hostname -f` | Print the fully qualified domain name |

**Linux:**

```bash
hostname
hostname -f
hostname -I
```

**macOS:** `hostname` and `hostname -f` work the same; `-I` is Linux-only.

**Release QA use:** Confirm which test or staging host a command ran on.

**Watch out:** Containers often have random host names; do not use the host
name as a stable environment identifier.

### `date`

**Frequent.** Print or format the current date and time.

| Usage | What it does |
|---|---|
| `date` | Print the local date and time |
| `date +%Y-%m-%dT%H:%M:%S%z` | Print an ISO-style timestamp |
| `date -d '1 hour ago'` | Parse a relative time (Linux) |

**Linux:**

```bash
date
date +%Y-%m-%dT%H:%M:%S%z
date -d '1 hour ago'
```

**macOS:** `date` and the `+` format work the same; the relative-time flag is
`date -v-1H`, not `-d`.

**Release QA use:** Timestamp a log excerpt or compare the local clock with a
server's certificate time.

**Watch out:** GNU and BSD `date` flags differ; `-d` is not portable.

### `uptime`

**Situational.** Show how long the system has been up and its load averages.

| Usage | What it does |
|---|---|
| `uptime` | Print uptime and 1, 5, and 15 minute load averages |

**Linux:**

```bash
uptime
```

**macOS:** Same command.

**Release QA use:** Check whether a test host rebooted during a long run.

**Watch out:** Load average is not CPU percentage; compare it with the number
of CPU cores.

### `df`

**Day-to-day.** Show free space on mounted filesystems.

| Flag | What it does |
|---|---|
| `-h` | Human-readable sizes |
| `-T` | Show the filesystem type (Linux) |
| `-i` | Show inode usage (Linux) |

**Linux:**

```bash
df -h
df -hT
df -i
```

**macOS:** `df -h` works; `-T` and `-i` are not portable.

**Release QA use:** Check free space before downloading a build or writing a
large log.

**Watch out:** A filesystem can be out of inodes while `df -h` still shows free
space; check `df -i` on Linux.

### `du`

**Day-to-day.** Show disk usage for files and directories.

| Flag | What it does |
|---|---|
| `-s` | Print only a summary |
| `-h` | Human-readable sizes |
| `--max-depth=1` | Limit the depth (Linux) |
| `-d 1` | Limit the depth (macOS) |

**Linux:**

```bash
du -sh artifacts
du -h --max-depth=1 releases
```

**macOS:** `du -sh artifacts` works; use `du -h -d 1 releases` for the depth
limit.

**Release QA use:** Find what filled the artifact or log volume.

**Watch out:** `du` walks the whole tree and can be slow on a huge directory;
scope it to the path you care about.

### `free`

**Day-to-day.** Show memory usage (Linux).

| Flag | What it does |
|---|---|
| `-h` | Human-readable sizes |
| `-m` | Show values in megabytes |
| `-s 5` | Repeat every five seconds |

**Linux:**

```bash
free -h
free -m
```

**macOS:** Not available on a standard Mac; use `vm_stat` and `top`.

**Release QA use:** Check memory pressure before a load test or after a long
soak test.

**Watch out:** Linux counts cache as free; read the `available` column, not
just `free`.

### `ps`

**Day-to-day.** List running processes.

| Usage | What it does |
|---|---|
| `ps aux` | Show all processes in BSD style |
| `ps -ef` | Show all processes in System V style |
| `ps -o pid,ppid,cmd -p 1234` | Choose columns for one PID |

**Linux:**

```bash
ps aux
ps -ef
ps -o pid,ppid,cmd -p 1234
```

**macOS:** Same commands; `ps aux`, `ps -ef`, and `-o` work.

**Release QA use:** Confirm the test service is running and find the PID to
inspect or stop.

**Watch out:** `ps aux | grep myapp` also matches the `grep` process; use
`grep [m]yapp` or `pgrep -af myapp`.

### `top`

**Day-to-day.** Show a live view of processes and resource use.

| Flag | What it does |
|---|---|
| `-b` | Batch mode, no interactive screen (Linux) |
| `-n 1` | Run one iteration (Linux) |
| `-p 1234` | Watch one PID (Linux) |
| `-l 1` | Run one sample (macOS) |

**Linux:**

```bash
top
top -b -n 1
top -p 1234
```

**macOS:** `top` works; use `top -l 1` for one sample, and `-pid` instead of
`-p`.

**Release QA use:** Watch CPU and memory during a test run, or capture one
batch snapshot for a bug report.

**Watch out:** `top` is interactive by default; use batch mode when writing
output to a file or a script.

## Part 2 — Files and Folders

### `mkdir`

**Day-to-day.** Create directories.

| Flag | What it does |
|---|---|
| `-p` | Create missing parent directories |
| `-v` | Print each directory created |

**Linux:**

```bash
mkdir -p releases/2026-11-18/logs
mkdir -v artifacts
```

**macOS:** Same commands.

**Release QA use:** Create a dated release directory and its log folder before
copying artifacts.

**Watch out:** Without `-p`, a missing parent makes the command fail.

### `touch`

**Frequent.** Create empty files or update timestamps.

| Flag | What it does |
|---|---|
| `-c` | Do not create the file if it is missing |
| `-t` | Set an explicit timestamp |

**Linux:**

```bash
touch artifacts/.keep
touch -c app.log
```

**macOS:** Same commands.

**Release QA use:** Create placeholder files or refresh a timestamp so sort and
find tests have predictable data.

**Watch out:** `touch` fails in a read-only directory; `-c` avoids creating a
file by accident.

### `cp`

**Day-to-day.** Copy files and directories.

| Flag | What it does |
|---|---|
| `-r` | Copy directories recursively |
| `-p` | Preserve mode, ownership, and timestamps |
| `-v` | Print each file copied |

**Linux:**

```bash
cp app.zip artifacts/
cp -r releases/2026-11-18 artifacts/
cp -p config.yml backups/
```

**macOS:** Same commands; `-r`, `-p`, and `-v` work the same.

**Release QA use:** Copy a build into the artifact folder while preserving its
timestamp for the release record.

**Watch out:** Copying a directory into an existing directory can nest it one
level deeper than expected; check the result with `ls`.

### `mv`

**Day-to-day.** Move or rename files and directories.

| Flag | What it does |
|---|---|
| `-i` | Ask before overwriting |
| `-v` | Print each move |

**Linux:**

```bash
mv app.zip artifacts/
mv build old-build
```

**macOS:** Same commands.

**Release QA use:** Rename a build by version or move old logs into an archive
directory.

**Watch out:** `mv` overwrites silently by default; use `-i` for important
files.

### `rm`

**Day-to-day.** Remove files and directories.

| Flag | What it does |
|---|---|
| `-r` | Remove directories recursively |
| `-i` | Ask before each removal |
| `-f` | Force removal without prompts |

**Linux:**

```bash
rm old.log
rm -r temp-build
rm -i artifacts/app.zip
```

**macOS:** Same commands; there is no trash or recycle bin on the command line.

**Release QA use:** Clean temporary build folders, but never delete the only
copy of a log or artifact that supports a bug report.

**Watch out:** `rm -rf` is permanent; scope the path carefully and never run it
against `/` or an unresolved variable.

### `ln`

**Frequent.** Create hard links or symbolic links.

| Flag | What it does |
|---|---|
| `-s` | Create a symbolic link |
| `-f` | Replace an existing link |

**Linux:**

```bash
ln -s releases/2026-11-18 current
ls -l current
```

**macOS:** Same commands.

**Release QA use:** Point a stable `current` link at the build under test.

**Watch out:** A relative symlink resolves from the link's directory, not your
working directory; use an absolute target or check with `readlink`.

### `find`

**Day-to-day.** Search for files by name, type, size, and modification time.

| Flag | What it does |
|---|---|
| `-name` | Match a filename pattern |
| `-type` | Filter by file type |
| `-size` | Filter by size |
| `-mtime` | Filter by modification time in days |
| `-maxdepth` | Limit how deep to search |

**Linux:**

```bash
find releases -maxdepth 2 -type f -name '*.zip'
find /var/log/myapp -type f -mtime -1
find artifacts -type f -size +100M
```

**macOS:** The same filters work; `-printf` is GNU-only and not portable.

**Release QA use:** Find recent logs, oversized artifacts, or files from the
current release window.

**Watch out:** `find` walks everything under the path; scope it with
`-maxdepth`, and treat `-delete` as destructive.

### `stat`

**Frequent.** Show file metadata: size, permissions, and timestamps.

| Flag | What it does |
|---|---|
| `-c` | Choose output fields (Linux) |
| `-f` | Choose output fields (macOS) |

**Linux:**

```bash
stat artifacts/app.zip
stat -c '%n %s %y' artifacts/app.zip
```

**macOS:** Use `stat artifacts/app.zip` or
`stat -f '%N %z %Sm' artifacts/app.zip`.

**Release QA use:** Check an artifact's size and modification time against the
build manifest.

**Watch out:** `-c` and `-f` are not interchangeable between GNU and BSD.

### `file`

**Frequent.** Identify a file's type from its contents.

| Flag | What it does |
|---|---|
| `-b` | Print the type without the filename |

**Linux:**

```bash
file artifact.zip
file -b app
```

**macOS:** Same commands.

**Release QA use:** Confirm an artifact is the expected type — a zip, an ELF
binary, or a shell script — before release.

**Watch out:** The extension does not prove the type; `file` reads the content.

### Reading paths

An **absolute path** starts at `/`, such as `/var/log/myapp/app.log`. A
**relative path** starts from your current directory, such as
`releases/2026-11-18`. `~` means your home directory, `.` means the current
directory, and `..` means the parent.

Globs expand before the command runs: `*` matches any characters, `?` matches
one character, and `[abc]` matches one of the listed characters. Quote a path
that contains spaces: `"artifacts/my build.zip"`.

## Part 3 — Viewing and Searching Text and Logs

### `cat`

**Day-to-day.** Print a file to the terminal.

| Flag | What it does |
|---|---|
| `-n` | Number the output lines |

**Linux:**

```bash
cat app.log
cat -n config.yml
```

**macOS:** Same commands.

**Release QA use:** Read a small config or a short artifact; use `less` or
`tail` for a large log.

**Watch out:** `cat` on a huge log floods the terminal and can hide the part
you need.

### `less`

**Day-to-day.** Page through a file and search inside it.

| Key | What it does |
|---|---|
| `/pattern` | Search forward |
| `n` | Next match |
| `G` | Go to the end |
| `g` | Go to the start |
| `q` | Quit |

**Linux:**

```bash
less /var/log/myapp/app.log
```

**macOS:** Same command.

**Release QA use:** Search a large log without loading all of it into the
terminal.

**Watch out:** `less` is interactive; use `grep` or `tail` in scripts.

### `head`

**Day-to-day.** Show the start of a file.

| Flag | What it does |
|---|---|
| `-n 20` | Show the first 20 lines |

**Linux:**

```bash
head -n 20 app.log
```

**macOS:** Same command.

**Release QA use:** Check the header of a log, CSV, or build manifest.

**Watch out:** `head` closes the pipe early; a producer may see a broken pipe.

### `tail`

**Day-to-day.** Show the end of a file and follow it as it grows.

| Flag | What it does |
|---|---|
| `-n 100` | Show the last 100 lines |
| `-f` | Follow the file |
| `-F` | Follow the file name across rotation |

**Linux:**

```bash
tail -n 100 /var/log/myapp/app.log
tail -f /var/log/myapp/app.log
tail -F /var/log/myapp/app.log
```

**macOS:** Same commands; `-f` and `-F` work the same.

**Release QA use:** Follow a service log during a smoke test, or attach the
last 100 lines to a bug report.

**Watch out:** `-f` can stop when the file is rotated or truncated; use `-F`
when rotation is possible.

### `grep`

**Day-to-day.** Search text for a pattern.

| Flag | What it does |
|---|---|
| `-i` | Ignore case |
| `-n` | Show line numbers |
| `-r` | Search a directory recursively |
| `-v` | Invert the match |
| `-c` | Count matching lines |

**Linux:**

```bash
grep -i error app.log
grep -rn 'timeout' /var/log/myapp
grep -v health app.log
```

**macOS:** Same flags; `-P` is GNU-only and not portable.

**Release QA use:** Find errors, exclude noisy health checks, and count how
often a message appears.

**Watch out:** `grep` exits 0 for a match, 1 for no match, and 2 for an error;
a script must distinguish "no match" from "bad pattern or unreadable file."

### `wc`

**Frequent.** Count lines, words, and bytes.

| Flag | What it does |
|---|---|
| `-l` | Count lines |
| `-w` | Count words |
| `-c` | Count bytes |

**Linux:**

```bash
wc -l app.log
grep -i error app.log | wc -l
```

**macOS:** Same commands.

**Release QA use:** Count errors or requests in a log.

**Watch out:** `wc -l` counts newline characters; a final line without a
newline is not counted.

### `cut`

**Frequent.** Extract fields or characters from each line.

| Flag | What it does |
|---|---|
| `-d` | Set the delimiter |
| `-f` | Choose fields |
| `-c` | Choose characters |

**Linux:**

```bash
cut -d' ' -f1 app.log
cut -d',' -f2,3 report.csv
```

**macOS:** Same commands.

**Release QA use:** Pull the timestamp or status code from a log or CSV.

**Watch out:** `-d` takes a single character; a multi-character delimiter needs
another tool.

### `sort`

**Day-to-day.** Sort lines.

| Flag | What it does |
|---|---|
| `-n` | Sort numerically |
| `-r` | Reverse the order |
| `-k` | Sort by a field |
| `-u` | Remove duplicate lines |

**Linux:**

```bash
sort app.log
sort -n counts.txt
sort -t',' -k3 -n report.csv
```

**macOS:** Same commands.

**Release QA use:** Order log lines or counts, and prepare input for `uniq`.

**Watch out:** The default sort is lexicographic; use `-n` for numbers.

### `uniq`

**Frequent.** Collapse adjacent duplicate lines.

| Flag | What it does |
|---|---|
| `-c` | Count each group |
| `-d` | Show only duplicate groups |
| `-u` | Show only unique lines |

**Linux:**

```bash
sort app.log | uniq -c
sort app.log | uniq -c | sort -nr | head
```

**macOS:** Same commands.

**Release QA use:** Count repeated error messages in a log.

**Watch out:** `uniq` only removes adjacent duplicates; sort the input first.

### `tee`

**Frequent.** Write output to the screen and to a file.

| Flag | What it does |
|---|---|
| `-a` | Append instead of overwrite |

**Linux:**

```bash
./run-tests.sh | tee artifacts/test.log
./run-tests.sh 2>&1 | tee -a artifacts/test.log
```

**macOS:** Same commands.

**Release QA use:** Keep a live view of a test run while saving the output as
evidence.

**Watch out:** `tee` writes as your user; check that the directory exists and
has space before a long run.

### Log triage pipeline

A safe way to find the most common errors in the last 1,000 lines:

```bash
tail -n 1000 /var/log/myapp/app.log \
  | grep -i error \
  | sort \
  | uniq -c \
  | sort -nr \
  | head -n 20
```

`tail` takes the recent window, `grep` keeps error lines, `sort` groups them,
`uniq -c` counts each group, the second `sort -nr` puts the largest count
first, and `head` shows the top 20. Every stage is a command in this part.

## Part 4 — Processes and Services

### Finding the process

Use `ps aux` or `ps -ef` from Part 1 to list processes, and `top` from Part 1
for a live view. The **PID** is the process ID; the **PPID** is its parent. A
quick way to find a named process is `pgrep -af myapp`, which prints the PID
and the command line without matching the `pgrep` process itself.

### `kill`

**Frequent.** Send a signal to a process.

| Usage | What it does |
|---|---|
| `kill 1234` | Send TERM to PID 1234 |
| `kill -TERM 1234` | Ask the process to stop cleanly |
| `kill -9 1234` | Force the process to stop |
| `kill -l` | List signal names |

**Linux:**

```bash
kill 1234
kill -TERM 1234
kill -9 1234
```

**macOS:** Same commands.

**Release QA use:** Stop a hung test process, preferring TERM so it can clean
up, and using KILL only when it will not exit.

**Watch out:** `kill -9` skips cleanup and can leave locks or partial files;
confirm the PID before you send a signal.

### `jobs`

**Frequent.** List the jobs started from the current shell.

| Flag | What it does |
|---|---|
| `-l` | Include PIDs |

**Linux:**

```bash
jobs
jobs -l
```

**macOS:** Same commands.

**Release QA use:** See which background test runs are still active in your
terminal.

**Watch out:** `jobs` shows only the current shell's jobs, not every process on
the machine.

### `bg`

**Situational.** Resume a suspended job in the background.

| Usage | What it does |
|---|---|
| `bg %1` | Continue job 1 in the background |

**Linux:**

```bash
bg %1
```

**macOS:** Same command.

**Release QA use:** Keep a long test run going while you inspect logs in the
same terminal.

**Watch out:** Job control is interactive only; it does not work the same way
inside a non-interactive script.

### `fg`

**Situational.** Bring a background or suspended job to the foreground.

| Usage | What it does |
|---|---|
| `fg %1` | Bring job 1 to the foreground |

**Linux:**

```bash
fg %1
```

**macOS:** Same command.

**Release QA use:** Return to a test run to watch its output after checking
something else.

**Watch out:** `Ctrl-Z` suspends the current job; use `bg` to continue it in the
background rather than leaving it stopped.

### `systemctl`

**Day-to-day.** Manage systemd services (Linux only).

| Usage | What it does |
|---|---|
| `systemctl status myapp` | Show service state and recent logs |
| `sudo systemctl restart myapp` | Restart the service |
| `systemctl is-active myapp` | Print active or inactive |

**Linux:**

```bash
systemctl status myapp --no-pager
sudo systemctl restart myapp
systemctl is-active myapp
```

**macOS:** Not available; use `launchctl` for services, for example
`launchctl list | grep myapp`.

**Release QA use:** Check whether the test service is active, restart it after a
configuration change, and confirm the new state.

**Watch out:** `systemctl` requires systemd; containers often do not run it.

### `journalctl`

**Day-to-day.** Read the systemd journal (Linux only).

| Flag | What it does |
|---|---|
| `-u myapp` | Filter to one service |
| `-f` | Follow new entries |
| `--since '1 hour ago'` | Limit by time |
| `-p err` | Show error priority |
| `-n 100` | Show the last 100 entries |
| `--no-pager` | Print directly instead of paging |

**Linux:**

```bash
journalctl -u myapp -n 100 --no-pager
journalctl -u myapp -f
journalctl -u myapp --since '1 hour ago' -p err
```

**macOS:** Use `log show --last 1h` for recent unified logs, or `log stream`
to follow them.

**Release QA use:** Read a service's logs without knowing which file it writes
to.

**Watch out:** The journal may be volatile or access-restricted; use `sudo`
only when the policy allows it.

### Service vs process

A **process** is a running program with a PID. A **service** is a background
program managed by the init system, such as a systemd unit. One service can
start several processes. `systemctl status` shows the unit; `ps` shows the
individual processes.

### Signals

| Signal | Meaning |
|---|---|
| `TERM` | Ask the process to stop cleanly |
| `KILL` | Force the process to stop; it cannot be caught |
| `HUP` | Hangup; many services reload their configuration |
| `INT` | Interrupt, usually from `Ctrl-C` |
| `STOP` / `CONT` | Pause and resume a process |

## Part 5 — Permissions and Ownership

### Reading `ls -l`

A long listing starts with a permission string such as `-rw-r--r--`. The first
character is the type (`-` file, `d` directory, `l` symlink). The next nine
characters are three triples: owner, group, and others, each read, write, and
execute. Then come the owner, group, size, modification time, and name.

For a directory, the execute bit means "can traverse or enter." A file can be
readable but still unreachable if a parent directory is not executable by your
user.

### `chmod`

**Day-to-day.** Change permissions.

| Usage | What it does |
|---|---|
| `chmod +x run-tests.sh` | Add execute for everyone |
| `chmod u+x run-tests.sh` | Add execute for the owner |
| `chmod 644 config.yml` | Owner read/write, group and others read |
| `chmod 755 run-tests.sh` | Owner read/write/execute, others read/execute |

**Linux:**

```bash
chmod +x run-tests.sh
chmod 644 config.yml
chmod 755 artifacts/run-tests.sh
```

**macOS:** Same commands.

**Release QA use:** Make a test script executable, or set read-only permissions
on an artifact that should not change.

**Watch out:** `chmod -R 777` is unsafe; give the minimum permissions the
process needs.

### `chown`

**Day-to-day.** Change a file's owner, and optionally its group.

| Usage | What it does |
|---|---|
| `chown user file` | Change the owner |
| `chown user:group file` | Change owner and group |
| `chown -R user:group dir` | Change recursively |

**Linux:**

```bash
sudo chown "$USER":"$USER" artifacts/app.zip
sudo chown -R "$USER":"$USER" releases/2026-11-18
```

**macOS:** Same commands; `$USER` works.

**Release QA use:** Fix ownership after copying artifacts from a container or
a root-run build job.

**Watch out:** Changing ownership requires root; never chown system paths just
to make one test pass.

### `chgrp`

**Frequent.** Change a file's group.

| Usage | What it does |
|---|---|
| `chgrp qa logs/app.log` | Change the group |
| `chgrp -R qa logs` | Change recursively |

**Linux:**

```bash
chgrp qa logs/app.log
chgrp -R qa logs
```

**macOS:** Same commands.

**Release QA use:** Give the QA group read access to a log directory.

**Watch out:** You must be a member of the target group, and the group change
does not add permissions by itself.

### `umask`

**Situational.** Show or set the default permission mask for new files.

| Usage | What it does |
|---|---|
| `umask` | Print the current mask |
| `umask 022` | New files get 644 and directories 755 |

**Linux:**

```bash
umask
umask 022
```

**macOS:** Same commands.

**Release QA use:** Understand why a freshly created log or artifact has the
permissions it does.

**Watch out:** `umask` subtracts permissions; it never adds them.

### `sudo`

**Day-to-day.** Run a command as another user, usually root.

| Usage | What it does |
|---|---|
| `sudo command` | Run as root |
| `sudo -u user command` | Run as another user |
| `sudo -l` | List your allowed sudo commands |

**Linux:**

```bash
sudo systemctl restart myapp
sudo -u qa cat /var/log/myapp/app.log
sudo -l
```

**macOS:** Same commands.

**Release QA use:** Restart a test service or read a root-owned log when the
environment expects it.

**Watch out:** `sudo` can change files as root and can hide permission problems
that users will hit; use it only when necessary.

### Permission denied

When a command returns `Permission denied`, check three things: whether your
user has the needed read, write, or execute bit (`ls -l`), whether your user is
in the owning group (`id`), and whether a parent directory is traversable. Use
`sudo` only when the task genuinely requires root.
