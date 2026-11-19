# Release QA Interview Topic 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `release-qa-interview/topic-03-linux-commands/` with a ten-part Linux command guide (side-by-side macOS notes), 100 Q&A, 150 MCQs, and a README for a junior-to-mid release QA interview.

**Architecture:** One task-based knowledge document built part by part, then two question files that mirror its ten parts and continuous numbering. Every command entry has a frequency badge, Linux examples, a macOS line, a release-QA use, and a common failure. Inline Python checks verify structure, counts, reveal blocks, duplicates, and the command-entry format after every task.

**Tech Stack:** GitHub-flavored Markdown, `<details>` reveal blocks, Python 3 checks, git.

**Spec:** `docs/superpowers/specs/2026-11-18-release-qa-interview-topic-03-design.md`

## Global Constraints

- Work on branch `release-qa-interview-topic-03`, created from `release-qa-interview-topic-02` at `2b549de`. Topic 2 is intentionally unmerged, so this branch is stacked.
- Folder: `release-qa-interview/topic-03-linux-commands/`.
- Files: `README.md`, `linux-commands.md`, `qa-100.md`, `mcq-150.md`.
- Knowledge parts: `## Part 1 — Orientation and System Information` through `## Part 10 — Release QA Workflows`, plus `## macOS Quick Reference`.
- Q&A counts: Part 1 = 8, 2 = 12, 3 = 14, 4 = 12, 5 = 10, 6 = 10, 7 = 8, 8 = 10, 9 = 8, 10 = 8; total 100.
- MCQ counts: Part 1 = 12, 2 = 18, 3 = 20, 4 = 18, 5 = 15, 6 = 15, 7 = 12, 8 = 15, 9 = 12, 10 = 13; total 150.
- Q&A numbering `Q1`–`Q100` continuous; MCQ numbering `1`–`150` continuous.
- Every answer sits inside `<details><summary>Show answer</summary>` … `</details>`.
- Every MCQ has exactly four options `A. `–`D. `, exactly one `**Correct answer: X.**` line, and an explanation.
- Frequency badges: **Day-to-day**, **Frequent**, **Situational**.
- Every command entry has a `**macOS:**` line: "Same commands" or the macOS equivalent.
- Each command entry has two or three Linux examples in a `bash` fence, one release-QA use, and one common failure.
- Exclude `awk` and `sed`; no shell scripting, kernel tuning, package management, or advanced editors.
- No near-duplicate stems within or across the question files.
- Correct-answer letters across 150 MCQs: 30–45 per letter.
- About 40% of MCQs are scenarios or command-output items.
- Examples are syntax-checked against standard GNU/Linux behavior but not executed on this Windows machine.

## Review Focus

1. **Wrong command or flag for the platform.** Each entry's Linux examples and macOS line must be accurate; `systemctl`/`journalctl`, `ip`/`ss`, and `free` are Linux-only and need a macOS equivalent.
2. **Missing or wrong frequency badge.** Every command entry uses exactly one of Day-to-day, Frequent, or Situational; the checker fails a bad entry.
3. **Unsafe examples.** No `rm -rf /`, no unquoted variables, no destructive command without a scoped path; examples use `/var/log/myapp`, `releases/`, and `artifacts/`.
4. **Duplicate stems.** The same command fact worded twice across the Q&A and MCQ banks makes the pack feel padded; the fuzzy duplicate scan catches address- and number-only differences.
5. **Off-level content.** `awk`, `sed`, scripts, and package management are out of scope; the forbidden-term check and final read enforce the junior-to-mid level.

## File Structure

- `release-qa-interview/topic-03-linux-commands/README.md` — purpose, files, study order, coverage table.
- `release-qa-interview/topic-03-linux-commands/linux-commands.md` — the ten-part command guide plus macOS quick reference.
- `release-qa-interview/topic-03-linux-commands/qa-100.md` — 100 open questions with hidden answers.
- `release-qa-interview/topic-03-linux-commands/mcq-150.md` — 150 four-option MCQs with hidden answers and explanations.

---

### Task 1: Scaffold, README, and Orientation Commands

**Files:**
- Create: `release-qa-interview/topic-03-linux-commands/README.md`
- Create: `release-qa-interview/topic-03-linux-commands/linux-commands.md`

**Interfaces:**
- Consumes: the approved design.
- Produces: the command-entry format, the README layout, and `check_notes.py` used by Tasks 2–6.

- [ ] **Step 1: Create `check_notes.py` in the execution workspace and run it; expect failure**

Base it on `check_notes.py` from Task 1 of
`docs/superpowers/plans/2026-11-18-release-qa-interview-topic-02.md`, adding the
command-entry loop described below. The checker reads `linux-commands.md` and:

- Checks the requested `--parts` headings exist.
- Checks all code fences are balanced.
- When `--toc` is passed, checks every `](#…)` link resolves.
- When `--macos-appendix` is passed, checks `## macOS Quick Reference` exists.
- For every `### \`command\`` heading, checks the section contains one of the three frequency badges, a `**macOS:**` line, and at least two ```` ``` ```` fences.
- Fails if the words `awk` or `sed` appear.
- Prints `parts: [...]`, `bad entries: [...]`, `notes checks passed`.

Run: `python <workspace>/check_notes.py --parts 1`
Expected: `FileNotFoundError` for `linux-commands.md`.

- [ ] **Step 2: Create `README.md`**

Include: title `# Release QA Interview Prep — Linux Commands`; the audience
(junior-to-mid release QA); a files table; a short study order (read a part,
then answer that part's Q&A and MCQs); the ten-part coverage table; a note that
Linux examples include the macOS equivalent side by side; and one line saying
later topics sit beside this folder. Keep it under 50 lines.

- [ ] **Step 3: Create `linux-commands.md` with front matter and Part 1**

Front matter:

```markdown
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
```

Add a short "How to read an entry" section explaining the frequency badges,
the flags table, the Linux examples, the `**macOS:**` line, the release-QA use,
and the "Watch out" line.

Then Part 1 with these command entries:
`pwd`, `ls`, `cd`, `whoami`, `id`, `uname`, `hostname`, `date`, `uptime`,
`df`, `du`, `free`, `ps`, `top`.

Use this format for each:

````markdown
### `tail`

**Day-to-day.** Show the end of a file; the standard way to watch a log.

| Flag | What it does |
|---|---|
| `-n 50` | Show the last 50 lines |
| `-f` | Follow new lines |
| `-F` | Follow across rotation |

**Linux:**

```bash
tail -n 100 /var/log/myapp/app.log
tail -f /var/log/myapp/app.log
```

**macOS:** Same commands; `tail -f` and `-F` work the same.

**Release QA use:** Follow a service log during a smoke test, or attach the
last 100 lines to a bug report.

**Watch out:** `Permission denied` means your user cannot read the file;
`No such file or directory` means the path or container is wrong.
````

For Linux-only commands, the macOS line names the equivalent, for example
`**macOS:** Not available on a standard Mac; use `vm_stat` and `top`.` for
`free`.

- [ ] **Step 4: Run the knowledge check**

Run: `python <workspace>/check_notes.py --parts 1`
Expected: `parts: [1]`, `bad entries: []`, and `notes checks passed`.

Read Part 1 and confirm the flags and the macOS lines are accurate.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/README.md release-qa-interview/topic-03-linux-commands/linux-commands.md && git commit -m "feat: add topic 3 Linux guide and orientation commands" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 2: Files, Folders, Text, and Logs

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/linux-commands.md`

**Interfaces:**
- Consumes: Task 1's command-entry format.
- Produces: `## Part 2 — Files and Folders` and `## Part 3 — Viewing and Searching Text and Logs`.

- [ ] **Step 1: Append Parts 2–3**

Part 2 command entries: `mkdir`, `touch`, `cp`, `mv`, `rm`, `ln`, `find`,
`stat`, `file`. Include path and glob examples, recursive copy, `find` by name,
size, and modification time, `stat` for timestamps and permissions, and safe
deletion. Add a plain `### Reading paths` section for absolute vs relative
paths and `~`.

Part 3 command entries: `cat`, `less`, `head`, `tail`, `grep`, `wc`, `cut`,
`sort`, `uniq`, `tee`. Include `grep` with `-i`, `-n`, `-r`, and `-v`, the
`grep` exit code, `tail -f` for logs, `sort | uniq -c` for counts, and a short
"log triage pipeline" section with a safe multi-command example.

- [ ] **Step 2: Run the knowledge check**

Run: `python <workspace>/check_notes.py --parts 1 2 3`
Expected: `parts: [1, 2, 3]`, `bad entries: []`, `notes checks passed`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/linux-commands.md && git commit -m "feat: add file, folder, and log commands" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 3: Processes, Services, and Permissions

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/linux-commands.md`

**Interfaces:**
- Consumes: Task 1's command-entry format.
- Produces: `## Part 4 — Processes and Services` and `## Part 5 — Permissions and Ownership`.

- [ ] **Step 1: Append Parts 4–5**

Part 4 command entries: `ps`, `top`, `kill`, `jobs`, `bg`, `fg`, `systemctl`,
`journalctl`. Include `ps aux` and `ps -ef` differences, `top` fields, signals
(`TERM`, `KILL`, `HUP`), `systemctl status/start/stop/restart`, and
`journalctl -u`, `-f`, `--since`, `-p err`, `-n`, `--no-pager`. macOS line:
`launchctl` for services and `log show` for logs.

Part 5 command entries: `chmod`, `chown`, `chgrp`, `umask`, `id`, `sudo`.
Include symbolic and numeric `chmod`, recursive `chown`, `umask` defaults, and
the permission-denied failure. Add a plain `### Reading ls -l` section that
explains the permission string, owner, group, and other.

- [ ] **Step 2: Run the knowledge check**

Run: `python <workspace>/check_notes.py --parts 1 2 3 4 5`
Expected: `parts: [1, 2, 3, 4, 5]`, `bad entries: []`, `notes checks passed`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/linux-commands.md && git commit -m "feat: add process, service, and permission commands" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 4: Disks, Memory, Archives, and Shell Mechanics

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/linux-commands.md`

**Interfaces:**
- Consumes: Task 1's command-entry format.
- Produces: `## Part 6 — Disks, Memory, and Archives` and `## Part 7 — Pipes, Redirection, Exit Codes, and Environment`.

- [ ] **Step 1: Append Parts 6–7**

Part 6 command entries: `df`, `du`, `free`, `tar`, `gzip`, `gunzip`, `zip`,
`unzip`, `sha256sum`. Include `df -h`, `du -sh`, `tar -czf` and `tar -xzf`,
`sha256sum` for artifact checks, and the disk-full failure. macOS line:
`vm_stat` for `free`.

Part 7: plain sections for pipes (`|`), output redirection (`>`, `>>`), error
redirection (`2>`, `2>&1`), and exit codes (`$?`), plus command entries for
`tee`, `env`, `export`, and a plain section on `PATH`. Include a safe example
such as `./run-tests.sh > artifacts/test.log 2>&1; echo $?` and explain that
`0` means success.

- [ ] **Step 2: Run the knowledge check**

Run: `python <workspace>/check_notes.py --parts 1 2 3 4 5 6 7`
Expected: `parts: [1, 2, 3, 4, 5, 6, 7]`, `bad entries: []`, `notes checks passed`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/linux-commands.md && git commit -m "feat: add disk, archive, and shell mechanics" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 5: SSH, File Transfer, curl, and Network Checks

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/linux-commands.md`

**Interfaces:**
- Consumes: Task 1's command-entry format.
- Produces: `## Part 8 — SSH and File Transfer` and `## Part 9 — curl and Network Checks`.

- [ ] **Step 1: Append Parts 8–9**

Part 8 command entries: `ssh`, `ssh-keygen`, `scp`, `sftp`, `rsync`. Add a plain
`### SSH config` section for `~/.ssh/config` and a plain `### SSH failures`
section for `Permission denied (publickey)`, host-key warnings, timeouts, and
wrong users. Include running a remote command, copying artifacts, and syncing
a build directory. macOS line: same commands; the built-in `rsync` may be old,
and Homebrew can install a newer one.

Part 9 command entries: `curl`, `ping`, `dig`, `ss`, `nc`. Include `curl -I`,
`-v`, `-X`, `-H`, `-d`, `-o`, `--max-time`, `--retry`, status-code checks,
auth, cookies, and TLS errors. Include `ping -c`, `dig +short`, `ss -tulpn`,
and `nc -vz`. macOS line: `ifconfig`/`netstat`/`lsof` instead of `ip`/`ss`;
`dig` and `curl` are the same.

- [ ] **Step 2: Run the knowledge check**

Run: `python <workspace>/check_notes.py --parts 1 2 3 4 5 6 7 8 9`
Expected: `parts: [1, 2, 3, 4, 5, 6, 7, 8, 9]`, `bad entries: []`, `notes checks passed`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/linux-commands.md && git commit -m "feat: add SSH, transfer, curl, and network checks" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 6: Release QA Workflows, macOS Quick Reference, and Full Notes Check

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/linux-commands.md`

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: `## Part 10 — Release QA Workflows`, `## macOS Quick Reference`, and a complete knowledge document with resolving TOC.

- [ ] **Step 1: Append Part 10 and the macOS quick reference**

Part 10 uses plain sections, not new command entries:

- Artifact checks: `ls -lh`, `find`, `sha256sum`, `tar -tzf`.
- Log triage: `tail -f`, `grep`, `journalctl -u`, `less`.
- Service status: `systemctl status`, `journalctl`, process checks.
- Port and endpoint checks: `ss`, `nc`, `curl -I`.
- Permission and disk checks: `ls -l`, `id`, `df -h`, `du -sh`.
- A short release-day checklist that ties the commands together.

Then `## macOS Quick Reference` with:

- Shared commands that work the same.
- `systemctl`/`journalctl` → `launchctl`/`log show`.
- `ip`/`ss` → `ifconfig`/`netstat`/`lsof`.
- `free` → `vm_stat`/`top`.
- `apt`/`dnf` → Homebrew.
- GNU vs BSD flag differences (`ls --color` vs `ls -G`, `grep -P`, `stat`,
  `date`, `readlink`).
- `/home` vs `/Users`; case-sensitive vs case-insensitive filesystems.

- [ ] **Step 2: Run the full knowledge check**

Run: `python <workspace>/check_notes.py --parts 1 2 3 4 5 6 7 8 9 10 --toc --macos-appendix`
Expected: `parts: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`, `toc unresolved: []`, `bad entries: []`, `notes checks passed`.

Read the macOS lines and confirm each command is either marked "Same" or has a
real equivalent.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/linux-commands.md && git commit -m "feat: complete the Linux guide and macOS reference" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 7: Q&A Parts 1–3

**Files:**
- Create: `release-qa-interview/topic-03-linux-commands/qa-100.md`

**Interfaces:**
- Consumes: the knowledge document and Task 1's heading style.
- Produces: the Q&A format; `check_qa.py`; `Q1`–`Q34`.

- [ ] **Step 1: Create `check_qa.py` and run it; expect failure**

Use the `check_qa.py` code from Task 1 of
`docs/superpowers/plans/2026-11-18-release-qa-interview-topic-01.md`, pointed at
`release-qa-interview/topic-03-linux-commands/qa-100.md`, with `--parts`,
`--total`, and `--toc`.

Run: `python <workspace>/check_qa.py --parts 1:8 2:12 3:14 --total 34`
Expected: `FileNotFoundError`.

- [ ] **Step 2: Create `qa-100.md` with front matter, TOC, and Parts 1–3**

Title: `# Release QA Interview Practice — Topic 3`. TOC links use the part
headings below with their counts.

Part 1, 8 questions:

- `pwd`, `cd` — 2
- `ls` and its flags — 1
- `whoami`, `id` — 1
- `uname`, `hostname` — 1
- `date`, `uptime` — 1
- `df`, `du` — 1
- `free` — 1

Part 2, 12 questions:

- `mkdir`, `touch` — 1
- `cp`, `mv` — 2
- `rm` and safe deletion — 2
- `ln` — 1
- `find` — 2
- `stat`, `file` — 2
- paths, globs, and `~` — 2

Part 3, 14 questions:

- `cat`, `less` — 2
- `head`, `tail`, `tail -f` — 3
- `grep` — 3 (basics, flags, exit code)
- `wc`, `cut` — 2
- `sort`, `uniq` — 2
- `tee` — 1
- log triage pipeline — 1

- [ ] **Step 3: Run the Q&A check**

Run: `python <workspace>/check_qa.py --parts 1:8 2:12 3:14 --total 34`
Expected: counts, total 34, sequential, details balanced 34/34, `expected matches: True`.

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/qa-100.md && git commit -m "feat: add Linux Q&A parts 1-3" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 8: Q&A Parts 4–6

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/qa-100.md`

**Interfaces:**
- Consumes: Task 7's format.
- Produces: `Q35`–`Q66`.

- [ ] **Step 1: Append Parts 4–6**

Part 4, 12 questions:

- `ps`, `ps aux` — 2
- `top` — 1
- `kill`, signals — 2
- `jobs`, `bg`, `fg` — 2
- `systemctl status/start/stop/restart` — 2
- `journalctl` and its flags — 2
- service vs process — 1

Part 5, 10 questions:

- reading `ls -l` — 1
- `chmod` symbolic — 2
- `chmod` numeric — 1
- `chown`, `chgrp` — 2
- `umask` — 1
- `id` — 1
- `sudo` — 1
- permission denied — 1

Part 6, 10 questions:

- `df` — 1
- `du` — 1
- `free` — 1
- `tar` create/extract — 2
- `gzip`/`gunzip` — 1
- `zip`/`unzip` — 1
- `sha256sum` — 1
- artifact checksum — 1
- disk full — 1

- [ ] **Step 2: Run the Q&A check**

Run: `python <workspace>/check_qa.py --parts 1:8 2:12 3:14 4:12 5:10 6:10 --total 66`
Expected: counts, total 66, sequential, details balanced 66/66.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/qa-100.md && git commit -m "feat: add Linux Q&A parts 4-6" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 9: Q&A Parts 7–10 and Full Check

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/qa-100.md`

**Interfaces:**
- Consumes: Task 7's format.
- Produces: `Q67`–`Q100`; a complete `qa-100.md` with resolving TOC.

- [ ] **Step 1: Append Parts 7–10**

Part 7, 8 questions:

- pipe `|` — 1
- `>` and `>>` — 1
- `2>` — 1
- `2>&1` — 1
- `$?` — 1
- `env`, `export` — 2
- `PATH` — 1

Part 8, 10 questions:

- `ssh` login and remote command — 2
- `ssh-keygen` and keys — 1
- `~/.ssh/config` — 1
- `scp` — 1
- `sftp` — 1
- `rsync` — 1
- host-key warning — 1
- `Permission denied (publickey)` — 1
- tunnels/port forwarding — 1

Part 9, 8 questions:

- `curl` GET and `-I` — 2
- `curl -v`, methods, headers, data — 2
- status codes and TLS errors — 1
- timeouts and retries — 1
- `ping` — 1
- `dig`, `ss`, `nc` — 1

Part 10, 8 questions:

- artifact check — 1
- checksum — 1
- log triage — 1
- service status — 1
- port/endpoint check — 1
- permission check — 1
- disk space — 1
- release-day checklist — 1

- [ ] **Step 2: Run the full Q&A check**

Run: `python <workspace>/check_qa.py --parts 1:8 2:12 3:14 4:12 5:10 6:10 7:8 8:10 9:8 10:8 --total 100 --toc`
Expected: exact counts, total 100, sequential, details 100/100, `toc unresolved: []`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/qa-100.md && git commit -m "feat: complete the 100-question Linux Q&A" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 10: MCQ Parts 1–3

**Files:**
- Create: `release-qa-interview/topic-03-linux-commands/mcq-150.md`

**Interfaces:**
- Consumes: the knowledge document and Task 7's heading style.
- Produces: the MCQ format; `check_mcq.py`; `MCQ 1`–`MCQ 50`.

- [ ] **Step 1: Create `check_mcq.py` and run it; expect failure**

Use the `check_mcq.py` code from Task 5 of
`docs/superpowers/plans/2026-11-18-release-qa-interview-topic-01.md`, pointed at
`release-qa-interview/topic-03-linux-commands/mcq-150.md`, with `--parts`,
`--total`, `--toc`, and `--letter-bounds`.

Run: `python <workspace>/check_mcq.py --parts 1:12 2:18 3:20 --total 50`
Expected: `FileNotFoundError`.

- [ ] **Step 2: Create `mcq-150.md` with front matter, TOC, and Parts 1–3**

Part 1, 12 MCQs: `pwd`/`cd`, `ls`, `whoami`/`id`, `uname`/`hostname`,
`date`/`uptime`, `df`, `du`, `free`, `ps`, `top`, flags, command output.

Part 2, 18 MCQs: `mkdir`/`touch`, `cp`, `mv`, `rm`, `ln`, `find` (name, size,
time), `stat`, `file`, paths, globs, recursive operations, safe deletion.

Part 3, 20 MCQs: `cat`, `less`, `head`, `tail`, `tail -f`, `grep` basics and
flags, `grep` exit code, `wc`, `cut`, `sort`, `uniq`, `tee`, log pipelines.

About 40% should be scenarios or command-output items.

- [ ] **Step 3: Run the MCQ check**

Run: `python <workspace>/check_mcq.py --parts 1:12 2:18 3:20 --total 50`
Expected: counts, total 50, sequential, no bad options or answers, details 50/50.

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/mcq-150.md && git commit -m "feat: add Linux MCQs parts 1-3" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 11: MCQ Parts 4–6

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/mcq-150.md`

**Interfaces:**
- Consumes: Task 10's format.
- Produces: `MCQ 51`–`MCQ 98`.

- [ ] **Step 1: Append Parts 4–6**

Part 4, 18 MCQs: `ps`, `ps aux`, `top`, `kill`, signals, `jobs`, `bg`/`fg`,
`systemctl`, `journalctl`, service vs process.

Part 5, 15 MCQs: `ls -l`, symbolic and numeric `chmod`, `chown`, `chgrp`,
`umask`, `id`, `sudo`, permission denied.

Part 6, 15 MCQs: `df`, `du`, `free`, `tar` create/extract, `gzip`/`gunzip`,
`zip`/`unzip`, `sha256sum`, artifact checks, disk full.

- [ ] **Step 2: Run the MCQ check**

Run: `python <workspace>/check_mcq.py --parts 1:12 2:18 3:20 4:18 5:15 6:15 --total 98`
Expected: counts, total 98, no bad options or answers, details 98/98.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/mcq-150.md && git commit -m "feat: add Linux MCQs parts 4-6" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 12: MCQ Parts 7–10 and Full Check

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/mcq-150.md`

**Interfaces:**
- Consumes: Task 10's format.
- Produces: `MCQ 99`–`MCQ 150`; a complete `mcq-150.md` with resolving TOC and a spread answer key.

- [ ] **Step 1: Append Parts 7–10**

Part 7, 12 MCQs: pipes, `>`, `>>`, `2>`, `2>&1`, `tee`, `$?`, `env`, `export`,
`PATH`.

Part 8, 15 MCQs: `ssh`, remote command, keys, config, `scp`, `sftp`, `rsync`,
host-key warnings, public-key failures, tunnels.

Part 9, 12 MCQs: `curl` GET, `-I`, `-v`, methods, headers, data, status codes,
TLS errors, timeouts, `ping`, `dig`, `ss`/`nc`.

Part 10, 13 MCQs: artifact checks, checksums, log triage, service status, port
checks, permission checks, disk space, release checklist scenarios.

- [ ] **Step 2: Run the full MCQ check**

Run: `python <workspace>/check_mcq.py --parts 1:12 2:18 3:20 4:18 5:15 6:15 7:12 8:15 9:12 10:13 --total 150 --toc --letter-bounds`
Expected: counts, total 150, sequential, no bad options or answers, details
150/150, `toc unresolved: []`, `letter bounds ok: True`.

If a letter falls outside 30–45, move the correct option in enough items to
rebalance, then rerun.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/mcq-150.md && git commit -m "feat: complete the 150-question Linux MCQ bank" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 13: Cross-File Verification, README, and Process Docs

**Files:**
- Modify: `release-qa-interview/topic-03-linux-commands/README.md` (only if stale)
- Verify: `linux-commands.md`, `qa-100.md`, `mcq-150.md`

**Interfaces:**
- Consumes: all four files from Tasks 1–12.
- Produces: a verified handover state with no duplicate stems, at least 40%
  scenario MCQs, no `awk`/`sed`, and a README matching the files.

- [ ] **Step 1: Create `check_content.py` and run it**

The checker must:

- Normalize stems across `qa-100.md` and `mcq-150.md` and fail on exact duplicates.
- Strip IPv4 addresses and numbers before a second duplicate pass, to catch
  templates that differ only by a host or count.
- Count scenario MCQs (stems starting with `A `, `An `, `After `, `When a `,
  `When an `, `During `, or containing `a team`, `a tester`, `a user`, `a
  developer`, `a project`, `a build`) and fail below 60/150.
- Grep all three content files for `\bawk\b` and `\bsed\b` and fail on any hit.
- Count `<details>`, `<summary>`, and `</details>` per question block and fail
  unless each is exactly one.

Run: `python <workspace>/check_content.py`
Expected: `duplicate stems: []`, `scenario MCQs: >= 60/150`, `content checks passed`.

- [ ] **Step 2: Read the bank for paraphrase duplicates and level**

Read all ten parts of both question files. Flag any two items testing the same
fact, any explanation that only restates the answer, any command claimed for
the wrong platform, and any item that is too advanced for a junior-to-mid
candidate. Fix in place and rerun the checks.

- [ ] **Step 3: Check the README against the files**

Confirm file names, counts, the study order, and the coverage table. Confirm
the README mentions the side-by-side macOS notes. Fix any stale line.

- [ ] **Step 4: Run the complete verification suite**

Run:

```bash
python <workspace>/check_notes.py --parts 1 2 3 4 5 6 7 8 9 10 --toc --macos-appendix
python <workspace>/check_qa.py --parts 1:8 2:12 3:14 4:12 5:10 6:10 7:8 8:10 9:8 10:8 --total 100 --toc
python <workspace>/check_mcq.py --parts 1:12 2:18 3:20 4:18 5:15 6:15 7:12 8:15 9:12 10:13 --total 150 --toc --letter-bounds
python <workspace>/check_content.py
```

All four must exit zero and print their pass line.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-03-linux-commands/ docs/superpowers/specs/2026-11-18-release-qa-interview-topic-03-design.md docs/superpowers/plans/2026-11-18-release-qa-interview-topic-03.md && git commit -m "docs: finalize release QA interview topic 3" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```
