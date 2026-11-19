# Release QA Interview Topic 3 — Design

**Date:** 2026-11-18
**Status:** Approved in conversation.

## Intent

A practical Linux command-line study pack for a junior-to-mid release QA
interview: a task-based reference the reader studies, then 100 Q&A and 150 MCQs
for self-testing. Linux and macOS are shown side by side, because the commands
are largely shared but some flags and system tools differ.

## Goals

- `linux-commands.md`: ten purpose-based parts. Each command entry has a
  frequency badge, what it does, two to four common flags, two or three example
  commands, one release-QA use, and one common failure.
- 100 Q&A with hidden answers of 2–5 sentences.
- 150 four-option MCQs with a hidden answer and explanation.
- A README with the study order and coverage table.
- A macOS line beside every command entry: "Same on macOS" when it is, or the
  equivalent command and flags when it differs.
- A macOS quick-reference appendix summarizing the main differences.

## Non-goals

- `awk`, `sed`, shell scripting, kernel tuning, package management, and
  advanced editors.
- Deep networking concepts; topic 2 is the reference for those.
- Running the commands in this Windows environment. Examples are
  syntax-verified against standard GNU/Linux behavior, not executed.

## Constraints

- Folder: `release-qa-interview/topic-03-linux-commands/`.
- Files: `README.md`, `linux-commands.md`, `qa-100.md`, `mcq-150.md`.
- Q&A counts by part: 8/12/14/12/10/10/8/10/8/8 = 100.
- MCQ counts by part: 12/18/20/18/15/15/12/15/12/13 = 150.
- Continuous numbering Q1–Q100 and MCQ 1–150.
- Four options A–D per MCQ, exactly one correct answer, and an explanation that
  names the nearest trap.
- Answers hidden in `<details>` blocks, same format as topics 1–2.
- Frequency badges: **Day-to-day**, **Frequent**, **Situational**.
- Side-by-side Linux and macOS coverage in every command entry; a macOS
  quick-reference appendix as a summary.
- No near-duplicate stems within or across the question files.
- Correct-answer letters spread 30–45 per letter.
- About 40% of MCQs are scenarios or command-output items.
- New-grad/junior-to-mid depth.

## Approaches considered

1. **Purpose-first parts with a frequency badge per command (chosen).** One
   canonical entry per command; the reader can study by task and prioritize by
   frequency.
2. **Frequency-first sections.** Day-to-day, Frequent, and Situational sections.
   Commands appear once, but task context is split across tiers.
3. **Flat alphabetical reference.** Easy lookup, but poor study order and no
   frequency signal.

## Coverage

| Part | Q&A | MCQ | Contents |
|---|---|---|---|
| 1. Orientation and system information | 8 | 12 | `pwd`, `ls`, `cd`, `whoami`, `id`, `uname`, `hostname`, `date`, `uptime`, `df`, `du`, `free`, `ps`, `top` |
| 2. Files and folders | 12 | 18 | `mkdir`, `touch`, `cp`, `mv`, `rm`, `ln`, `find`, `stat`, `file` |
| 3. Viewing and searching text and logs | 14 | 20 | `cat`, `less`, `head`, `tail`, `grep`, `wc`, `cut`, `sort`, `uniq`, `tee` |
| 4. Processes and services | 12 | 18 | `ps`, `top`, `kill`, `jobs`, `bg`, `fg`, `systemctl`, `journalctl` |
| 5. Permissions and ownership | 10 | 15 | `ls -l`, `chmod`, `chown`, `chgrp`, `umask`, `id`, `sudo` |
| 6. Disks, memory, and archives | 10 | 15 | `df`, `du`, `free`, `tar`, `gzip`, `gunzip`, `zip`, `unzip`, `sha256sum` |
| 7. Pipes, redirection, exit codes, and environment | 8 | 12 | `|`, `>`, `>>`, `2>`, `2>&1`, `tee`, `$?`, `env`, `export`, `PATH` |
| 8. SSH and file transfer | 10 | 15 | `ssh`, `ssh-keygen`, `~/.ssh/config`, `scp`, `sftp`, `rsync` |
| 9. curl and network checks | 8 | 12 | `curl`, `ping`, `dig`, `ss`, `nc`; brief concepts, topic 2 reference |
| 10. Release QA workflows | 8 | 13 | artifact and checksum checks, log triage, service status, port checks, permission checks, disk space |

## Command entry format

Each command gets:

- A frequency badge: Day-to-day, Frequent, or Situational.
- One sentence on what it does.
- A flags table with two to four common flags.
- Two or three Linux example commands in a `bash` fence, using consistent
  sample paths such as `/var/log/myapp/app.log`, `releases/`, and `artifacts/`.
- A macOS line beside the examples: "Same on macOS" when the command works
  unchanged, or the equivalent macOS command and flags when it differs.
- One release-QA use.
- One common failure, such as `Permission denied`, `No such file or directory`,
  or `command not found`.

## macOS quick reference

Every command entry has a side-by-side macOS line. The appendix is a one-page
summary of the shared commands and the main differences:

- `systemctl` / `journalctl` → `launchctl` / `log show`
- `ip` / `ss` → `ifconfig` / `netstat` / `lsof`
- `free` → `vm_stat` / `top`
- `apt` / `dnf` → Homebrew (`brew`)
- GNU vs BSD flag differences, such as `ls --color` vs `ls -G`, `grep -P`,
  `stat`, `date`, and `readlink`
- `/home` vs `/Users`; case-sensitive vs case-insensitive filesystems

## Verification

Inline Python checks after each task: part counts, continuous numbering,
reveal-block balance, MCQ option sets and one answer line, TOC anchors,
duplicate normalized stems, answer-letter distribution, and a check that
`awk` and `sed` do not appear as covered commands. A final read checks command
accuracy, every macOS side-by-side line, and the new-grad level. Examples are
syntax-checked against standard documentation but not executed.
