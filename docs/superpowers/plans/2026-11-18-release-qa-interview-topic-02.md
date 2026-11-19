# Release QA Interview Topic 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `release-qa-interview/topic-02-basic-networking/` with a five-part networking knowledge document, 100 Q&A, 150 MCQs, and a README for a new-grad release QA interview.

**Architecture:** One knowledge document built part by part, then two question files that mirror its five parts and continuous numbering. Inline Python checks verify structure, subnet arithmetic, port mappings, counts, reveal blocks, duplicates, and scenario share after every task.

**Tech Stack:** GitHub-flavored Markdown, `<details>` reveal blocks, Python 3 checks, git.

**Spec:** `docs/superpowers/specs/2026-11-18-release-qa-interview-topic-02-design.md`

## Global Constraints

- Work on branch `release-qa-interview-topic-02`, created from `release-qa-interview-topic-01` at `e8a9cce`. Topic 1 is intentionally unmerged, so this branch contains both topics; do not merge or push without the user's choice.
- Folder: `release-qa-interview/topic-02-basic-networking/`.
- Files: `README.md`, `networking-basics.md`, `qa-100.md`, `mcq-150.md`.
- Knowledge doc parts: `## Part 1 — Networking Fundamentals and Models` through `## Part 5 — Troubleshooting and Commands`.
- Q&A counts: Part 1 = 15, Part 2 = 15, Part 3 = 25, Part 4 = 25, Part 5 = 20; total 100.
- MCQ counts: Part 1 = 20, Part 2 = 25, Part 3 = 40, Part 4 = 35, Part 5 = 30; total 150.
- Q&A numbering `Q1`–`Q100` continuous; MCQ numbering `1`–`150` continuous.
- Every answer sits inside `<details><summary>Show answer</summary>` … `</details>`.
- Every MCQ has exactly four options `A. `–`D. `, exactly one `**Correct answer: X.**` line, and an explanation.
- Part heading format for questions: `## Part N — {Title} ({count} questions)`.
- New-grad depth: definitions, comparisons, small `/24`–`/28` subnetting arithmetic, command-output recognition, simple scenarios. No OSPF, BGP, MPLS, vendor certification depth, or advanced VLSM.
- Commands are labeled with the platform they work on: Windows, macOS, or Linux.
- No near-duplicate stems within or across the two question files.
- Correct-answer letters across 150 MCQs: each letter appears 30–45 times.
- About 40% of MCQs are scenarios or command-output items.
- README counts, file names, and usage instructions must match the built files.

## Review Focus

1. **Subnet arithmetic is wrong.** Network, broadcast, first usable, last usable, mask, block size, and host counts must match the `/24`–`/28` table and worked examples; the table checker recomputes every row.
2. **A command is wrong for its platform.** `ipconfig` is Windows, `ip addr` is Linux, `ifconfig` is macOS/older Linux, `tracert` is Windows, `traceroute` is macOS/Linux; every command block carries a platform label and is read for accuracy.
3. **A protocol or port is mismatched.** DNS 53, DHCP 67/68, HTTP 80, HTTPS 443, SSH 22, SMTP 25, POP3 110, IMAP 143, NTP 123, SNMP 161/162; the port-table checker enforces the required rows.
4. **Reworded duplicates.** Two items testing the same fact with different wording make the bank feel padded; the duplicate scan and the final read catch this.
5. **Off-level content.** Deep TLS handshake internals, routing-protocol configuration, and vendor commands are out of scope for a new grad; the final read checks for them.

## File Structure

- `release-qa-interview/topic-02-basic-networking/README.md` — purpose, files, how to use, coverage table.
- `release-qa-interview/topic-02-basic-networking/networking-basics.md` — the five-part knowledge document.
- `release-qa-interview/topic-02-basic-networking/qa-100.md` — 100 open questions with hidden answers.
- `release-qa-interview/topic-02-basic-networking/mcq-150.md` — 150 four-option MCQs with hidden answers and explanations.

---

### Task 1: Scaffold and Networking Fundamentals

**Files:**
- Create: `release-qa-interview/topic-02-basic-networking/README.md`
- Create: `release-qa-interview/topic-02-basic-networking/networking-basics.md`

**Interfaces:**
- Consumes: the approved design.
- Produces: the knowledge-doc heading and table conventions, the README layout, and the `check_notes.py` checker used by Tasks 2–5.

- [ ] **Step 1: Create `check_notes.py` in the execution workspace and run it; expect failure**

```python
#!/usr/bin/env python3
"""Structure, subnet, and port checks for networking-basics.md."""
import argparse
import pathlib
import re
import sys
from ipaddress import ip_network

PATH = pathlib.Path(
    "release-qa-interview/topic-02-basic-networking/networking-basics.md"
)


def slug(heading):
    heading = re.sub(r"[^\w\s-]", "", heading.strip().lower())
    return heading.replace(" ", "-")


def parse_table(text, header):
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip().startswith("|") and header in line:
            rows = []
            for row in lines[index + 2:]:
                if not row.strip().startswith("|"):
                    break
                rows.append(
                    [cell.strip() for cell in row.strip().strip("|").split("|")]
                )
            return rows
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parts", nargs="*", type=int, default=[])
    parser.add_argument("--toc", action="store_true")
    parser.add_argument("--subnets", action="store_true")
    parser.add_argument("--ports", action="store_true")
    args = parser.parse_args()

    text = PATH.read_text(encoding="utf-8")
    failures = []

    found = {int(n) for n, _ in re.findall(r"^## Part (\d+) — (.+)$", text, re.M)}
    print("parts:", sorted(found))
    if args.parts and not set(args.parts) <= found:
        failures.append(f"missing parts: {sorted(set(args.parts) - found)}")

    fences = text.count("```")
    print("code fences:", fences, "even:", fences % 2 == 0)
    if fences % 2:
        failures.append("unbalanced code fences")

    if args.toc:
        headings = {slug(h) for h in re.findall(r"^## (.+)$", text, re.M)}
        links = re.findall(r"\]\(#([^)]+)\)", text)
        unresolved = [link for link in links if link not in headings]
        print("toc unresolved:", unresolved)
        if unresolved:
            failures.append(f"unresolved TOC anchors: {unresolved}")

    if args.subnets:
        rows = parse_table(
            text, "| CIDR | Subnet mask | Block size | Networks in a /24 | Usable hosts |"
        )
        bad = []
        for cidr, mask, block, networks, hosts in rows:
            prefix = int(cidr.strip("/"))
            expected_block = 2 ** (32 - prefix)
            expected_mask = f"255.255.255.{256 - expected_block}"
            expected_networks = 2 ** (prefix - 24)
            expected_hosts = expected_block - 2
            if (mask, int(block), int(networks), int(hosts)) != (
                expected_mask,
                expected_block,
                expected_networks,
                expected_hosts,
            ):
                bad.append(cidr)
        print("subnet table rows:", len(rows), "bad:", bad)
        if len(rows) != 5 or bad:
            failures.append(f"subnet table wrong or incomplete: {bad}")

        examples = parse_table(
            text, "| Subnet | Network | First usable | Last usable | Broadcast |"
        )
        bad_examples = []
        for cidr, network, first, last, broadcast in examples:
            net = ip_network(cidr, strict=False)
            expected = (
                str(net.network_address),
                str(net.network_address + 1),
                str(net.broadcast_address - 1),
                str(net.broadcast_address),
            )
            if (network, first, last, broadcast) != expected:
                bad_examples.append(cidr)
        print("worked examples:", len(examples), "bad:", bad_examples)
        if len(examples) < 8 or bad_examples:
            failures.append(f"worked examples wrong or incomplete: {bad_examples}")

    if args.ports:
        rows = parse_table(text, "| Port | Protocol | Service |")
        required = {
            "22": "SSH",
            "25": "SMTP",
            "53": "DNS",
            "67/68": "DHCP",
            "80": "HTTP",
            "110": "POP3",
            "123": "NTP",
            "143": "IMAP",
            "161/162": "SNMP",
            "443": "HTTPS",
        }
        found_ports = {port: service for port, _, service in rows}
        missing = [
            port
            for port, service in required.items()
            if found_ports.get(port, "").upper() != service
        ]
        print("port table rows:", len(rows), "missing or wrong:", missing)
        if missing:
            failures.append(f"port table missing or wrong: {missing}")

    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print("notes checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Run: `python <workspace>/check_notes.py --parts 1`
Expected: `FileNotFoundError` for `networking-basics.md`.

- [ ] **Step 2: Create `README.md`**

Include: title `# Release QA Interview Prep — Networking`; one sentence naming
the audience (new grad, junior-to-mid); a files table (`networking-basics.md`,
`qa-100.md` — 100 Q&A, `mcq-150.md` — 150 MCQs); a how-to-use section (read the
knowledge doc, answer first, click Show answer); the five-part coverage table
from the spec; and one line saying later topics sit beside this folder. Keep it
under 45 lines.

- [ ] **Step 3: Create `networking-basics.md` with front matter and Part 1**

Front matter:

```markdown
# Basic Networking for Release QA

A plain-English networking primer for a new-grad release QA interview.

## Contents

- [Part 1 — Networking Fundamentals and Models](#part-1--networking-fundamentals-and-models)
- [Part 2 — Topologies and Devices](#part-2--topologies-and-devices)
- [Part 3 — Addressing and Subnetting](#part-3--addressing-and-subnetting)
- [Part 4 — Protocols and Ports](#part-4--protocols-and-ports)
- [Part 5 — Troubleshooting and Commands](#part-5--troubleshooting-and-commands)
```

Then Part 1 with these subsections:

- What a network is — nodes, links, packets, LAN/MAN/WAN/PAN, intranet vs internet
- Client-server vs peer-to-peer
- The OSI model — all seven layers, plain-English role of each
- The TCP/IP model — four layers, mapping to OSI
- Encapsulation and the PDU names (data, segment, packet, frame, bits)
- Bandwidth, latency, throughput, jitter, packet loss

Use short paragraphs, tables where a comparison is clearer, and at least one
text diagram of the two models side by side. No question blocks yet.

- [ ] **Step 4: Run the knowledge check**

Run: `python <workspace>/check_notes.py --parts 1`
Expected: `parts: [1]`, an even code-fence count (0 or 2 depending on whether
the model diagram is fenced), and `notes checks passed`.

Read Part 1 and confirm the OSI layer names are correct, the TCP/IP mapping is
consistent, and no advanced routing content appears.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/README.md release-qa-interview/topic-02-basic-networking/networking-basics.md && git commit -m "feat: add topic 2 networking folder and fundamentals" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 2: Topologies and Devices

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/networking-basics.md`

**Interfaces:**
- Consumes: Task 1's heading conventions.
- Produces: `## Part 2 — Topologies and Devices`.

- [ ] **Step 1: Append Part 2**

Cover:

- Physical vs logical topology
- Bus, star, ring, mesh (full and partial), tree, and hybrid topologies, each
  with a one-line diagram, a strength, and a failure mode
- Devices: hub, switch, router, access point, modem, firewall, proxy, load
  balancer, with the layer each mainly works at
- Collision domains vs broadcast domains; a short VLAN explanation

Keep every device and topology at new-grad depth. No vendor configuration.

- [ ] **Step 2: Run the knowledge check**

Run: `python <workspace>/check_notes.py --parts 1 2`
Expected: `parts: [1, 2]`, fences even, `notes checks passed`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/networking-basics.md && git commit -m "feat: add network topologies and devices" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 3: Addressing and Subnetting

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/networking-basics.md`

**Interfaces:**
- Consumes: Task 1's conventions and the `--subnets` check.
- Produces: `## Part 3 — Addressing and Subnetting` with the exact two tables below.

- [ ] **Step 1: Append Part 3**

Cover IPv4 format and octets; public vs private ranges, loopback, link-local,
and APIPA; subnet masks and CIDR; network, broadcast, first usable, last usable;
the host-count formula `2^h - 2`; a step-by-step subnetting method; default
gateway and routing basics; NAT; and IPv6 format, shortening, and address types
at a basic level.

Include this exact table:

```markdown
| CIDR | Subnet mask | Block size | Networks in a /24 | Usable hosts |
|---|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 1 | 254 |
| /25 | 255.255.255.128 | 128 | 2 | 126 |
| /26 | 255.255.255.192 | 64 | 4 | 62 |
| /27 | 255.255.255.224 | 32 | 8 | 30 |
| /28 | 255.255.255.240 | 16 | 16 | 14 |
```

Include this exact worked-examples table:

```markdown
| Subnet | Network | First usable | Last usable | Broadcast |
|---|---|---|---|---|
| 192.168.1.0/26 | 192.168.1.0 | 192.168.1.1 | 192.168.1.62 | 192.168.1.63 |
| 192.168.1.64/26 | 192.168.1.64 | 192.168.1.65 | 192.168.1.126 | 192.168.1.127 |
| 192.168.1.128/26 | 192.168.1.128 | 192.168.1.129 | 192.168.1.190 | 192.168.1.191 |
| 192.168.1.192/26 | 192.168.1.192 | 192.168.1.193 | 192.168.1.254 | 192.168.1.255 |
| 192.168.1.0/27 | 192.168.1.0 | 192.168.1.1 | 192.168.1.30 | 192.168.1.31 |
| 192.168.1.32/27 | 192.168.1.32 | 192.168.1.33 | 192.168.1.62 | 192.168.1.63 |
| 192.168.1.0/28 | 192.168.1.0 | 192.168.1.1 | 192.168.1.14 | 192.168.1.15 |
| 192.168.1.240/28 | 192.168.1.240 | 192.168.1.241 | 192.168.1.254 | 192.168.1.255 |
```

Add one fully worked `/26` example in prose, showing the binary block size,
network address, broadcast address, and usable range.

- [ ] **Step 2: Run the knowledge check with subnet validation**

Run: `python <workspace>/check_notes.py --parts 1 2 3 --subnets`
Expected: `subnet table rows: 5 bad: []`, `worked examples: 8 bad: []`, `notes checks passed`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/networking-basics.md && git commit -m "feat: add addressing and subnetting" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 4: Protocols and Ports

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/networking-basics.md`

**Interfaces:**
- Consumes: Task 1's conventions and the `--ports` check.
- Produces: `## Part 4 — Protocols and Ports` with the exact port table below.

- [ ] **Step 1: Append Part 4**

Cover TCP vs UDP, the three-way handshake, flags, reliability and ordering;
ports and sockets; HTTP and HTTPS methods and status codes; TLS and
certificates at a high level; DNS record types and resolution; DHCP DORA;
ARP; ICMP; SSH, FTP/SFTP, SMTP/IMAP/POP3, NTP, and SNMP.

Include this exact table:

```markdown
| Port | Protocol | Service |
|---|---|---|
| 20/21 | TCP | FTP |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | UDP/TCP | DNS |
| 67/68 | UDP | DHCP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 123 | UDP | NTP |
| 143 | TCP | IMAP |
| 161/162 | UDP | SNMP |
| 443 | TCP | HTTPS |
| 445 | TCP | SMB |
| 3306 | TCP | MySQL |
| 3389 | TCP | RDP |
| 5432 | TCP | PostgreSQL |
| 6379 | TCP | Redis |
| 8080 | TCP | HTTP alternative |
```

- [ ] **Step 2: Run the knowledge check with port validation**

Run: `python <workspace>/check_notes.py --parts 1 2 3 4 --ports`
Expected: `port table rows: 18 missing or wrong: []`, `notes checks passed`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/networking-basics.md && git commit -m "feat: add protocols and ports" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 5: Troubleshooting and Commands

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/networking-basics.md`

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: `## Part 5 — Troubleshooting and Commands`; a complete knowledge document with all five parts and resolving TOC anchors.

- [ ] **Step 1: Append Part 5**

Cover the diagnostic ladder: scope → link → IP → DNS → route → port → TLS →
HTTP → application. For each rung, give the symptom, the command, and how to
read the result:

- Windows: `ipconfig /all`, `ping`, `tracert`, `nslookup`, `netstat -ano`,
  `route print`, `arp -a`, `curl.exe`, `Test-NetConnection`, `Resolve-DnsName`
- macOS: `ifconfig`, `ping`, `traceroute`, `dig`, `netstat`, `route -n get`,
  `arp -a`, `curl`, `nc`, `openssl s_client`
- Linux: `ip addr`, `ip route`, `ping`, `traceroute`, `dig`, `ss`, `ip neigh`,
  `curl`, `nc`, `tcpdump`, `openssl s_client`

Include a symptom → likely-layer table, a short "what is not a network bug"
section, and a bug-report template with environment, steps, expected, actual,
evidence, and suspected layer. Put every command block under a bold platform
label.

- [ ] **Step 2: Run the full knowledge check**

Run: `python <workspace>/check_notes.py --parts 1 2 3 4 5 --toc`
Expected: `parts: [1, 2, 3, 4, 5]`, `toc unresolved: []`, `notes checks passed`.

Read the command sections and confirm each command is available on the platform
it is filed under, and that no vendor configuration appears.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/networking-basics.md && git commit -m "feat: complete networking knowledge document" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 6: Q&A Parts 1–2

**Files:**
- Create: `release-qa-interview/topic-02-basic-networking/qa-100.md`

**Interfaces:**
- Consumes: the knowledge document and Task 1's heading style.
- Produces: the Q&A format every later question task follows; `check_qa.py`; `Q1`–`Q30`.

- [ ] **Step 1: Create `check_qa.py` in the execution workspace and run it; expect failure**

Use the `check_qa.py` code from Task 1 of
`docs/superpowers/plans/2026-11-18-release-qa-interview-topic-01.md`, pointed at
`release-qa-interview/topic-02-basic-networking/qa-100.md`, with arguments
`--parts`, `--total`, and `--toc`. It must print part counts, total,
sequential numbering, reveal-tag balance, TOC unresolved links, and
`expected matches: True`, and exit non-zero on any mismatch.

Run: `python <workspace>/check_qa.py --parts 1:15 2:15 --total 30`
Expected: `FileNotFoundError` for `qa-100.md`.

- [ ] **Step 2: Create `qa-100.md` with front matter, TOC, and Parts 1–2**

Front matter title: `# Release QA Interview Practice — Topic 2`.
TOC links:

```markdown
- [Part 1 — Networking Fundamentals and Models (15 questions)](#part-1--networking-fundamentals-and-models-15-questions)
- [Part 2 — Topologies and Devices (15 questions)](#part-2--topologies-and-devices-15-questions)
- [Part 3 — Addressing and Subnetting (25 questions)](#part-3--addressing-and-subnetting-25-questions)
- [Part 4 — Protocols and Ports (25 questions)](#part-4--protocols-and-ports-25-questions)
- [Part 5 — Troubleshooting and Commands (20 questions)](#part-5--troubleshooting-and-commands-20-questions)
```

Part 1 subtopics and counts:

- Network types and components — 4
- Client-server vs peer-to-peer — 2
- OSI and TCP/IP models — 5
- Encapsulation — 2
- Bandwidth, latency, and throughput — 2

Part 2 subtopics and counts:

- Topologies — 7
- Devices — 5
- Collision domains, broadcast domains, and VLANs — 3

Question format is `### Subtopic`, `#### Qn. stem`, then the hidden answer
block. Answers are 2–5 sentences and use a concrete example where it helps.

- [ ] **Step 3: Run the Q&A check**

Run: `python <workspace>/check_qa.py --parts 1:15 2:15 --total 30`
Expected: `counts: {1: 15, 2: 15}`, `total: 30`, `sequential: True`,
`details balanced: True 30 30`, `expected matches: True`.

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/qa-100.md && git commit -m "feat: add networking Q&A parts 1-2" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 7: Q&A Parts 3–4

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/qa-100.md`

**Interfaces:**
- Consumes: Task 6's format.
- Produces: `Q31`–`Q80`.

- [ ] **Step 1: Append Parts 3–4**

Part 3 subtopics and counts:

- IPv4 basics — 5
- Public, private, and special addresses — 4
- Masks and CIDR — 4
- Subnetting calculations — 8
- Default gateway, routing, and NAT — 3
- IPv6 basics — 1

Part 4 subtopics and counts:

- TCP vs UDP and the handshake — 6
- Ports — 3
- DNS — 4
- DHCP — 2
- HTTP, HTTPS, and TLS — 5
- ARP and ICMP — 2
- SSH, FTP/SFTP, email, NTP, and SNMP — 3

Number continuously `Q31`–`Q80`. For subnetting questions, state the address
and prefix in the stem and show the calculation in the answer.

- [ ] **Step 2: Run the Q&A check**

Run: `python <workspace>/check_qa.py --parts 1:15 2:15 3:25 4:25 --total 80`
Expected: `counts: {1: 15, 2: 15, 3: 25, 4: 25}`, `total: 80`,
`sequential: True`, `details balanced: True 80 80`, `expected matches: True`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/qa-100.md && git commit -m "feat: add networking Q&A parts 3-4" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 8: Q&A Part 5 and TOC Validation

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/qa-100.md`

**Interfaces:**
- Consumes: Task 6's format.
- Produces: `Q81`–`Q100`; a complete `qa-100.md` with all TOC anchors resolving.

- [ ] **Step 1: Append Part 5**

Subtopics and counts:

- The diagnostic ladder — 4
- Commands and what they show — 8
- Reading command output — 4
- Bug reports and what is not a network bug — 4

Number continuously `Q81`–`Q100`.

- [ ] **Step 2: Run the full Q&A check**

Run: `python <workspace>/check_qa.py --parts 1:15 2:15 3:25 4:25 5:20 --total 100 --toc`
Expected: exact counts, `total: 100`, `sequential: True`,
`details balanced: True 100 100`, `toc unresolved: []`, `expected matches: True`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/qa-100.md && git commit -m "feat: complete the 100-question networking Q&A" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 9: MCQ Parts 1–2

**Files:**
- Create: `release-qa-interview/topic-02-basic-networking/mcq-150.md`

**Interfaces:**
- Consumes: the knowledge document and Task 6's heading style.
- Produces: the MCQ format every later task follows; `check_mcq.py`; `MCQ 1`–`MCQ 45`.

- [ ] **Step 1: Create `check_mcq.py` in the execution workspace and run it; expect failure**

Use the `check_mcq.py` code from Task 5 of
`docs/superpowers/plans/2026-11-18-release-qa-interview-topic-01.md`, pointed at
`release-qa-interview/topic-02-basic-networking/mcq-150.md`, with arguments
`--parts`, `--total`, `--toc`, and `--letter-bounds`. It must print part counts,
total, sequential numbering, bad option sets, bad answer lines, reveal-tag
balance, answer distribution, TOC unresolved links, letter bounds, and
`expected matches: True`, and exit non-zero on any mismatch.

Run: `python <workspace>/check_mcq.py --parts 1:20 2:25 --total 45`
Expected: `FileNotFoundError` for `mcq-150.md`.

- [ ] **Step 2: Create `mcq-150.md` with front matter, TOC, and Parts 1–2**

Front matter title: `# Release QA Interview MCQs — Topic 2`.
TOC links:

```markdown
- [Part 1 — Networking Fundamentals and Models (20 questions)](#part-1--networking-fundamentals-and-models-20-questions)
- [Part 2 — Topologies and Devices (25 questions)](#part-2--topologies-and-devices-25-questions)
- [Part 3 — Addressing and Subnetting (40 questions)](#part-3--addressing-and-subnetting-40-questions)
- [Part 4 — Protocols and Ports (35 questions)](#part-4--protocols-and-ports-35-questions)
- [Part 5 — Troubleshooting and Commands (30 questions)](#part-5--troubleshooting-and-commands-30-questions)
```

Part 1 subtopics and counts:

- Network types and components — 4
- Client-server vs peer-to-peer — 2
- OSI and TCP/IP models — 8
- Encapsulation — 3
- Bandwidth, latency, and throughput — 3

Part 2 subtopics and counts:

- Topologies — 10
- Devices — 9
- Collision domains, broadcast domains, and VLANs — 6

Question format is `### Subtopic`, `#### MCQ n. stem`, four options `A.`–`D.`,
then the hidden `**Correct answer: X.**` explanation. About 40% of this part
should be scenarios or command-output items.

- [ ] **Step 3: Run the MCQ check**

Run: `python <workspace>/check_mcq.py --parts 1:20 2:25 --total 45`
Expected: `counts: {1: 20, 2: 25}`, `total: 45`, `sequential: True`,
`bad option sets: []`, `bad answer lines: []`,
`details balanced: True 45 45`, `expected matches: True`.

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/mcq-150.md && git commit -m "feat: add networking MCQs parts 1-2" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 10: MCQ Part 3 — Addressing and Subnetting

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/mcq-150.md`

**Interfaces:**
- Consumes: Task 9's MCQ format.
- Produces: `MCQ 46`–`MCQ 85`.

- [ ] **Step 1: Append Part 3**

Subtopics and counts:

- IPv4 basics — 8
- Public, private, and special addresses — 5
- Masks and CIDR — 7
- Subnetting calculations — 12
- Default gateway, routing, and NAT — 5
- IPv6 basics — 3

Number continuously `MCQ 46`–`MCQ 85`. Keep subnetting arithmetic small
(`/24`–`/28`), state the address and prefix in the stem, and show the step in
the explanation. At least six items should be calculation questions with
unambiguous numeric answers.

- [ ] **Step 2: Run the MCQ check**

Run: `python <workspace>/check_mcq.py --parts 1:20 2:25 3:40 --total 85`
Expected: `counts: {1: 20, 2: 25, 3: 40}`, `total: 85`, `sequential: True`,
`bad option sets: []`, `bad answer lines: []`,
`details balanced: True 85 85`, `expected matches: True`.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/mcq-150.md && git commit -m "feat: add networking MCQ part 3 on subnetting" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 11: MCQ Parts 4–5 and Final Validation

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/mcq-150.md`

**Interfaces:**
- Consumes: Task 9's MCQ format.
- Produces: `MCQ 86`–`MCQ 150`; a complete `mcq-150.md` with all TOC anchors resolving and a spread answer key.

- [ ] **Step 1: Append Parts 4–5**

Part 4 subtopics and counts:

- TCP vs UDP and the handshake — 8
- Ports — 5
- DNS — 6
- DHCP — 3
- HTTP, HTTPS, and TLS — 8
- ARP and ICMP — 3
- Other protocols — 2

Part 5 subtopics and counts:

- The diagnostic ladder — 5
- Commands — 10
- Reading command output — 8
- Bug reports and what is not a network bug — 5
- Scenario diagnosis — 2

Number continuously `MCQ 86`–`MCQ 150`.

- [ ] **Step 2: Run the full MCQ check**

Run: `python <workspace>/check_mcq.py --parts 1:20 2:25 3:40 4:35 5:30 --total 150 --toc --letter-bounds`
Expected: `counts: {1: 20, 2: 25, 3: 40, 4: 35, 5: 30}`, `total: 150`,
`sequential: True`, `bad option sets: []`, `bad answer lines: []`,
`details balanced: True 150 150`, `toc unresolved: []`,
`letter bounds ok: True`, `expected matches: True`.

If a letter falls outside 30–45, move the correct option in enough items to
rebalance, then rerun.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/mcq-150.md && git commit -m "feat: complete the 150-question networking MCQ bank" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 12: Cross-File Verification, README, and Process Docs

**Files:**
- Modify: `release-qa-interview/topic-02-basic-networking/README.md` (only if counts or links are stale)
- Verify: `networking-basics.md`, `qa-100.md`, `mcq-150.md`

**Interfaces:**
- Consumes: all four files from Tasks 1–11.
- Produces: a verified handover state with no duplicate stems, at least 40% scenario MCQs, no advanced-routing content, and a README matching the files.

- [ ] **Step 1: Create `check_content.py` in the execution workspace and run the cross-file checks**

The checker must:

- Normalize stems across `qa-100.md` and `mcq-150.md` and fail on exact duplicates.
- Count scenario MCQs (stems starting with `A `, `An `, `After `, `When a `,
  `When an `, `During `, or containing `a team`, `a tester`, `a user`, `a
  customer`, `a developer`, `a project`, `a build`) and fail below 60/150.
- Grep both question files for `kanban`, `OSPF`, `BGP`, `MPLS`, `Cisco`,
  `Juniper`, `Fortinet`, and `Palo Alto` and fail on any hit.
- Count `<details>`, `<summary>`, and `</details>` per question block and fail
  unless each is exactly one.

Run: `python <workspace>/check_content.py`
Expected: `duplicate stems: []`, `scenario MCQs: >= 60/150`, `content checks passed`.

- [ ] **Step 2: Read the bank for paraphrase duplicates and level**

Read all five parts of both question files. Flag any two items testing the same
fact, any explanation that only restates the answer, any command claimed for
the wrong platform, and any item that is too advanced for a new grad. Fix in
place and rerun the checks.

- [ ] **Step 3: Check the README against the files**

Confirm file names, counts, and the coverage table match what was built; confirm
the how-to-use text mentions the knowledge document and the reveal blocks. Fix
any stale line.

- [ ] **Step 4: Run the complete verification suite**

Run:

```bash
python <workspace>/check_notes.py --parts 1 2 3 4 5 --toc --subnets --ports
python <workspace>/check_qa.py --parts 1:15 2:15 3:25 4:25 5:20 --total 100 --toc
python <workspace>/check_mcq.py --parts 1:20 2:25 3:40 4:35 5:30 --total 150 --toc --letter-bounds
python <workspace>/check_content.py
```

All four must exit zero and print their pass line.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/wshuhao/AI_Study" && git add release-qa-interview/topic-02-basic-networking/ docs/superpowers/specs/2026-11-18-release-qa-interview-topic-02-design.md docs/superpowers/plans/2026-11-18-release-qa-interview-topic-02.md && git commit -m "docs: finalize release QA interview topic 2" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"
```
