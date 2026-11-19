# Release QA Interview Prep — Linux Commands

Practical Linux command-line skills for a junior-to-mid release QA interview.
Linux examples include the macOS equivalent beside them.

## Files

| File | Contents |
|---|---|
| `linux-commands.md` | Ten-part command guide with side-by-side macOS notes |
| `qa-100.md` | 100 open questions with hidden answers |
| `mcq-150.md` | 150 multiple-choice questions with hidden answers and explanations |

## Study order

1. Read one part of `linux-commands.md`.
2. Answer the matching part of `qa-100.md`.
3. Run the matching part of `mcq-150.md` and read every explanation.

## Coverage

| Part | Q&A | MCQs | Topic |
|---|---|---|---|
| 1. Orientation and system information | 8 | 12 | `pwd`, `ls`, `cd`, `id`, `uname`, `date`, `df`, `du`, `free`, `ps`, `top` |
| 2. Files and folders | 12 | 18 | `mkdir`, `touch`, `cp`, `mv`, `rm`, `ln`, `find`, `stat`, `file` |
| 3. Viewing and searching text and logs | 14 | 20 | `cat`, `less`, `head`, `tail`, `grep`, `wc`, `cut`, `sort`, `uniq`, `tee` |
| 4. Processes and services | 12 | 18 | `ps`, `top`, `kill`, `jobs`, `systemctl`, `journalctl` |
| 5. Permissions and ownership | 10 | 15 | `ls -l`, `chmod`, `chown`, `umask`, `id`, `sudo` |
| 6. Disks, memory, and archives | 10 | 15 | `df`, `du`, `free`, `tar`, `gzip`, `zip`, `sha256sum` |
| 7. Pipes, redirection, exit codes, and environment | 8 | 12 | `|`, `>`, `2>&1`, `$?`, `env`, `export`, `PATH` |
| 8. SSH and file transfer | 10 | 15 | `ssh`, keys, `scp`, `sftp`, `rsync` |
| 9. curl and network checks | 8 | 12 | `curl`, `ping`, `dig`, `ss`, `nc` |
| 10. Release QA workflows | 8 | 13 | artifact checks, log triage, service and port checks |

Later topics will sit beside this folder as `topic-04-…` and so on.
