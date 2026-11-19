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
