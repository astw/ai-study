#!/usr/bin/env python3
"""Verify the larger-prefix extension and the existing topic 2 pack."""
import pathlib
import re
import sys
from ipaddress import ip_network

BASE = pathlib.Path("release-qa-interview/topic-02-basic-networking")


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


def fuzzy(stem):
    stem = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "<addr>", stem)
    stem = re.sub(r"[^a-z0-9<>/ ]", "", stem.lower())
    return re.sub(r"\s+", " ", stem).strip()


def main():
    notes = (BASE / "networking-basics.md").read_text(encoding="utf-8")
    qa = (BASE / "qa-100.md").read_text(encoding="utf-8")
    mcq = (BASE / "mcq-150.md").read_text(encoding="utf-8")
    extra = (BASE / "larger-prefixes-practice.md").read_text(encoding="utf-8")
    readme = (BASE / "README.md").read_text(encoding="utf-8")
    failures = []

    parts = sorted({int(n) for n in re.findall(r"^## Part (\d+) —", notes, re.M)})
    print("notes parts:", parts)
    if parts != [1, 2, 3, 4, 5]:
        failures.append(f"notes parts {parts}")

    fences = notes.count("```")
    print("notes fences:", fences, "even:", fences % 2 == 0)
    if fences % 2:
        failures.append("notes fences unbalanced")

    headings = {slug(h) for h in re.findall(r"^## (.+)$", notes, re.M)}
    links = re.findall(r"\]\(#([^)]+)\)", notes)
    unresolved = [link for link in links if link not in headings]
    print("notes toc unresolved:", unresolved)
    if unresolved:
        failures.append(f"notes toc {unresolved}")

    subnet_rows = parse_table(
        notes, "| CIDR | Subnet mask | Block size | Networks in a /24 | Usable hosts |"
    )
    print("subnet table rows:", len(subnet_rows))
    if len(subnet_rows) != 5:
        failures.append("subnet table incomplete")

    examples = parse_table(
        notes, "| Subnet | Network | First usable | Last usable | Broadcast |"
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
        failures.append(f"worked examples {bad_examples}")

    ports = parse_table(notes, "| Port | Protocol | Service |")
    print("port table rows:", len(ports))
    if len(ports) != 18:
        failures.append("port table incomplete")

    qa_nums = [int(n) for n in re.findall(r"^#### Q(\d+)\.", qa, re.M)]
    mcq_nums = [int(n) for n in re.findall(r"^#### MCQ (\d+)\.", mcq, re.M)]
    print("main counts:", len(qa_nums), len(mcq_nums))
    if len(qa_nums) != 100 or len(mcq_nums) != 150:
        failures.append("main bank counts changed")

    extra_q = [int(n) for n in re.findall(r"^#### Q(\d+)\.", extra, re.M)]
    extra_m = [int(n) for n in re.findall(r"^#### MCQ (\d+)\.", extra, re.M)]
    print("extension counts:", len(extra_q), len(extra_m))
    if len(extra_q) != 10 or extra_q != list(range(1, 11)):
        failures.append(f"extension Q&A counts {extra_q}")
    if len(extra_m) != 10 or extra_m != list(range(1, 11)):
        failures.append(f"extension MCQ counts {extra_m}")

    for label, text in (("extension", extra), ("Q&A main", qa), ("MCQ main", mcq)):
        if text.count("<details>") != text.count("</details>"):
            failures.append(f"{label} reveal tags unbalanced")

    qa_section = extra.split("## Multiple-choice questions", 1)[0]
    extra_q_blocks = re.split(r"^#### Q\d+\.", qa_section, flags=re.M)[1:]
    extra_m_blocks = re.split(r"^#### MCQ \d+\.", extra, flags=re.M)[1:]
    for number, block in enumerate(extra_q_blocks, 1):
        if (
            block.count("<details>") != 1
            or block.count("<summary>") != 1
            or block.count("</details>") != 1
        ):
            failures.append(f"extension Q{number} reveal tags")
    for number, block in enumerate(extra_m_blocks, 1):
        if re.findall(r"^([A-D])\. ", block, re.M) != list("ABCD"):
            failures.append(f"extension MCQ{number} options")
        if len(re.findall(r"\*\*Correct answer: [A-D]\.\*\*", block)) != 1:
            failures.append(f"extension MCQ{number} answer line")

    extra_headings = {slug(h) for h in re.findall(r"^## (.+)$", extra, re.M)}
    extra_links = re.findall(r"\]\(#([^)]+)\)", extra)
    extra_unresolved = [link for link in extra_links if link not in extra_headings]
    print("extension toc unresolved:", extra_unresolved)
    if extra_unresolved:
        failures.append(f"extension toc {extra_unresolved}")

    all_stems = (
        re.findall(r"^#### Q\d+\. (.+)$", qa, re.M)
        + re.findall(r"^#### Q\d+\. (.+)$", extra, re.M)
        + re.findall(r"^#### MCQ \d+\. (.+)$", mcq, re.M)
        + re.findall(r"^#### MCQ \d+\. (.+)$", extra, re.M)
    )
    exact = {}
    exact_dups = []
    for stem in all_stems:
        key = re.sub(r"[^a-z0-9 ]", "", stem.lower()).strip()
        if key in exact:
            exact_dups.append(stem)
        exact[key] = True
    print("exact duplicate stems:", exact_dups)
    if exact_dups:
        failures.append(f"exact duplicates {exact_dups}")

    fuzzy_seen = {}
    fuzzy_dups = []
    for stem in all_stems:
        key = fuzzy(stem)
        if key in fuzzy_seen:
            fuzzy_dups.append((fuzzy_seen[key], stem))
        fuzzy_seen[key] = stem
    print("fuzzy duplicate pairs:", len(fuzzy_dups))
    if fuzzy_dups:
        failures.append(f"fuzzy duplicates {fuzzy_dups}")

    if "larger-prefixes-practice.md" not in readme:
        failures.append("README missing extension file")
    if "10 Q&A and 10 MCQs" not in readme:
        failures.append("README missing extension counts")

    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print("extension checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
