# Release QA Interview Topic 2 — Design

**Date:** 2026-11-18
**Status:** Approved by the user in conversation.

## Intent

A basic-networking study pack for a new-grad / junior-to-mid release QA
interview: a condensed knowledge document, then a self-test Q&A and MCQ bank.
The reader should be able to explain how a network works, read an address and
subnet, name the common protocols, and troubleshoot a failed request with
commands.

## Goals

- A standalone `networking-basics.md` of roughly 700–900 lines covering
  fundamentals, topologies, addressing and subnetting, protocols, and
  troubleshooting.
- 100 interview-style Q&A with hidden answers of 2–5 sentences.
- 150 four-option MCQs with a hidden answer and explanation.
- A README tying the three files together.
- Plain English, new-grad depth, cross-platform commands (Windows, macOS,
  Linux).

## Non-goals

- OSPF, BGP, MPLS, and other advanced routing protocols.
- Vendor certification depth, packet-level protocol analysis, or tool-specific
  configuration.
- Advanced VLSM and IPv6 subnetting beyond the basics.
- Kanban or project-management content.
- Rewriting or re-leveling topic 1.

## Constraints

- Folder: `release-qa-interview/topic-02-basic-networking/`.
- Files: `README.md`, `networking-basics.md`, `qa-100.md`, `mcq-150.md`.
- Q&A counts by part: 15/15/25/25/20; MCQ counts: 20/25/40/35/30.
- Continuous numbering Q1–Q100 and MCQ 1–150.
- Four options A–D per MCQ, exactly one correct answer, explanation names the
  nearest trap.
- Answers hidden in `<details>` blocks, same format as topic 1.
- Subnetting arithmetic stays small (/24–/28) and every worked example shows the
  method.
- Commands are labeled with the platform they work on; no vendor-specific tools.
- No near-duplicate stems within or across the question files.
- Correct-answer letters spread roughly evenly (30–45 per letter).
- New-grad depth: definitions, comparisons, small calculations, command-output
  recognition, simple scenarios.

## Approaches considered

1. **Standalone condensed knowledge doc (chosen).** One folder is
   interview-ready; some material repeats the existing `tcp-ip-for-qa.md`.
2. **Supplement to `tcp-ip-for-qa.md`.** No repetition, but the reader needs
   two files and the interview framing is split.
3. **Full rewrite of the networking material.** Most complete, but duplicates a
   1,160-line guide and exceeds the new-grad scope.

## Coverage

| Part | Q&A | MCQ | Contents |
|---|---|---|---|
| 1. Fundamentals and models | 15 | 20 | network types, client-server vs peer-to-peer, OSI vs TCP/IP, encapsulation, bandwidth/latency/throughput |
| 2. Topologies and devices | 15 | 25 | bus, star, ring, mesh, tree, hybrid; physical vs logical; hub, switch, router, access point, firewall, load balancer, proxy |
| 3. Addressing and subnetting | 25 | 40 | IPv4, public/private, CIDR, masks, network/broadcast/host, /24–/28 subnetting, default gateway, IPv6 basics |
| 4. Protocols and ports | 25 | 35 | TCP/UDP, handshake, ports, HTTP/HTTPS, DNS, DHCP, ARP, ICMP, TLS, SSH, FTP/SFTP, email, NTP, SNMP |
| 5. Troubleshooting and commands | 20 | 30 | diagnostic ladder, cross-platform commands, output reading, common failure patterns, bug reports |

## Question rules

- Q&A: one concept per question; 2–5 sentence answer; an example where it
  clarifies.
- MCQ: stem, four options, one correct, plausible distractors; 1–3 sentence
  explanation; about 40% scenarios or command-output items; no "all of the
  above".
- Subnetting items include the small arithmetic needed to make the answer
  unambiguous; the explanation shows the step.
- Part headings carry their counts; TOC anchors match.

## Verification

Inline Python checks after each task: per-part counts, continuous numbering,
reveal-block balance, MCQ option sets and one answer line, TOC anchors,
duplicate normalized stems, answer-letter distribution, and a subnet-table
check that recomputes the documented /24–/28 network, broadcast, and host
values. A final read checks tone, duplicate ideas, and command accuracy.
