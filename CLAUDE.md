# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A content repository, not an application. It holds three long-form beginner guides: one introduces AI and Claude Code, with a self-contained HTML slide deck condensed from it; one introduces TCP/IP and related networking for QA work; and one introduces Playwright browser testing for QA, using the flashcards project from the AI guide as its running example. It also includes a runnable local MCP demo in `mcp-demo/`, used by Part 4.5 of the AI guide. The files were written by Claude Code at the user's request. The AI guide's purpose is onboarding: after reading, a newcomer should be able to start working with AI — explain what an LLM is and where it fails, write a working prompt, install and run Claude Code, and turn repeated work into skills, subagents, and structured workflows. The networking guide's purpose is the same kind of onboarding for QA: after reading, a newcomer should be able to explain how a request travels, read basic network configuration, test common network conditions, and write a reproducible network bug report. The Playwright guide should leave a newcomer able to install Playwright for Python, write and debug a real browser test, and explain what belongs in E2E testing versus lower layers. Judge content changes against those outcomes, not just against correctness. There is no build system, package manager, test suite, or compilation step — the Markdown and HTML files are the deliverables and are edited directly.

| File | Role |
|---|---|
| `README.md` | Reader-facing entry point: what is in the folder, who it is for, how to read it, how to open the deck, and an index of the companion QA guides. |
| `using-ai-from-zero-to-claude-code.md` | The AI handbook (source of truth). ~3,200 lines: 8 parts plus appendices A–F. |
| `tcp-ip-for-qa.md` | Standalone TCP/IP, DNS, DHCP, and VPN guide for QA beginners. ~1,500 lines: 7 parts plus appendices A–F. |
| `playwright-for-qa.md` | Standalone Playwright for Python guide for QA beginners, built around the flashcards example. ~1,400 lines: 10 parts plus appendices A–F. |
| `mcp-demo/` | Runnable local MCP server over SQLite (`server.py`), a no-Claude-Code smoke test (`smoke_test.py`), `requirements.txt`, and setup README. |
| `ai-claude-code-slides.html` | 40-slide deck as an Artifact fragment: begins at `<title>`, has no `<html>`/`<head>`/`<body>` wrappers, and carries `claude:viewport-fit-sides`. This is the file published through the Artifact tool. |
| `ai-claude-code-slides-standalone.html` | The same deck wrapped in a complete HTML document for opening locally or sharing as a file. |

## The two deck files must stay identical apart from the wrapper

`ai-claude-code-slides-standalone.html` is exactly `ai-claude-code-slides.html` plus a 12-line prologue (`<!doctype html>` through a small base `<style>`) and the closing `</head><body>` / `</body></html>` tags. Any edit to one deck must be mirrored in the other. Verify with:

```bash
diff <(sed 's/[[:space:]]*$//' ai-claude-code-slides.html) \
     <(sed 's/[[:space:]]*$//' ai-claude-code-slides-standalone.html)
```

The only expected output is those wrapper lines. A larger diff means the files have drifted.

## Working with the slide deck

- Everything lives in one file: inline CSS, inline JavaScript, and no assets except Google Fonts (IBM Plex Sans, IBM Plex Mono, Literata).
- Each slide is `<section class="slide" data-title="…" data-section="…" aria-hidden="true">`. The deck has 40 slides in six sections: Introduction (3), Part 01 · Understand (8), Part 02 · Ask (7), Part 03 · Operate (8), Part 04 · Build (9), Part 05 · Apply (5).
- Speaker notes live in `<div class="notes" hidden>` inside the owning slide; the notes panel renders `.notes` from the current slide.
- The script at the bottom derives the slide count, counter, progress bar, section label, and contents overlay from the DOM. Adding or removing a slide mostly requires only the `<section>` element with `data-title`/`data-section`; keep the visible `<!-- NN -->` numbering comments in order.
- Deep links use `#slide-N` (1-based) and `history.replaceState` keeps the hash in sync.
- Keyboard: → / PageDown / Space next; ← / PageUp / Shift+Space previous; Home / End; N for notes; O for contents; Esc closes notes or the overlay.
- The color palette is declared three times — `:root` (light), `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])`, and `:root[data-theme="dark"]`. Change colors in all three.

Preview by opening the standalone file directly in a browser (no server needed):

```powershell
Start-Process .\ai-claude-code-slides-standalone.html
```

Count slides after structural edits:

```bash
grep -c '<section class="slide' ai-claude-code-slides.html
```

## Working with the AI handbook

- Audience: people new to AI, written specifically for college students with no coding or terminal experience. The prose is second person, plain English, and assumes no prior knowledge. Keep that register; every section should leave the reader able to do something they could not do before.
- Structure is rigid: `# Part N` chapters with numbered `## N.M` sections, then appendices A–F. The Contents list at the top uses hand-written GitHub-style anchors; update it whenever headings change.
- The running example is Maya, a first-year student turning PSY 101 lecture notes into flashcards in a `flashcards/` folder. That project — `flashcards.py`, `cards.md`, `quiz.html`, its `.claude/` commands, skills, and agents — is teaching material only and does not exist in this repository. Do not go looking for it. The Playwright guide reuses the same project and quiz contract; keep the described behavior (one card, Show answer, Next card) consistent across guides.
- Appendix C contains copy-pasteable templates (CLAUDE.md, slash command, skill); Appendix A is the command cheat sheet. When a command, flag, or keybinding changes in the body, update the appendix too.
- Claude Code command, flag, and keybinding references are dated "Version 1.0 · November 2026" and must stay accurate. Verify against current Claude Code behavior rather than inventing syntax.
- Third-party tool details are equally version-sensitive: the handbook documents OpenSpec 2.0 (skills such as `/openspec-propose`, not the removed `/opsx:*` commands) and Superpowers 7.x. Check upstream documentation before changing those sections.
- The MCP demo in Part 4.5 is explained in the handbook but implemented in `mcp-demo/`. Keep the tool names, commands, and behavior in sync between the handbook, `mcp-demo/server.py`, and `mcp-demo/README.md`.
- The demo uses the MCP Python SDK 2.x (`mcp.server.mcpserver.MCPServer`, not `FastMCP` from 1.x) and `claude mcp add`. Keep the server code and commands tested against the current SDK and Claude Code; the demo uses only sample data and no credentials.

## Working with the TCP/IP guide

- Audience: the same complete beginners, but the goal is readiness for QA work rather than AI tooling. Keep the prose second person, plain English, and free of unexplained jargon.
- Structure: `# Part N` chapters with numbered `## N.M` sections, then appendices A–F. The Contents list uses hand-written GitHub-style anchors; update it whenever headings change.
- The guide's spine is the diagnostic ladder — scope → link → IP → DNS → route → port → TLS → HTTP → application. New material should fit that model and keep the QA test-matrix, lab, and bug-report sections practical.
- Networking facts are stable, but keep commands and tool syntax current across Windows, macOS, and Linux. Prefer commands that work without extra installs and label anything that requires a lab or authorization.
- Do not add a slide deck for this guide unless the user asks; it is currently a standalone Markdown document.

## Working with the Playwright guide

- Audience: the same complete beginners, now learning browser automation for QA. The guide assumes only basic Python (variables, functions, imports) and teaches the rest.
- Technical choice: Playwright's **Python** API with `pytest` and `pytest-playwright`, matching the flashcards project. The guide notes that TypeScript/JavaScript is the most common industry choice and that concepts transfer.
- Running example: Maya's flashcards project from the AI handbook (`cards.md`, `flashcards.py`, `quiz.html`). The guide includes a representative `quiz.html` fixture because the real `flashcards/` folder is not in this repository. Do not present the fixture as the actual generated file.
- Keep every Python example syntactically valid and every Playwright API claim verified against the official Python docs. Code that depends on an API-backed variant of the quiz must stay clearly labeled as such; the static fixture does not call `/api/cards` and has no loading/error states.
- Structure: `# Part N` chapters with numbered `## N.M` sections, then appendices A–F. Update the Contents anchors when headings change.
- Do not add a slide deck for this guide unless the user asks.

## Verification and tooling

There is no build or lint command; the guides are the product. These checks catch the common breakage:

````bash
# Every Markdown file must have balanced code fences (each count should be even)
grep -c '```' using-ai-from-zero-to-claude-code.md tcp-ip-for-qa.md playwright-for-qa.md

# Every Python example in the AI handbook and Playwright guide must compile
python - <<'PY'
import pathlib, re

for name in ("using-ai-from-zero-to-claude-code.md", "playwright-for-qa.md"):
    text = pathlib.Path(name).read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)```", text, re.S)
    for i, block in enumerate(blocks, 1):
        compile(block, f"{name}-block-{i}", "exec")
    print(f"{name}: {len(blocks)} Python blocks compile")
PY

# The runnable MCP demo must compile
python -m py_compile mcp-demo/server.py mcp-demo/smoke_test.py
````

Run the heredoc with the Bash tool. Internal anchors are hand-written; after changing a heading, check the Contents links. The deck's sync and slide-count checks are in the slide-deck section.

After installing `mcp-demo/requirements.txt`, `cd mcp-demo && python smoke_test.py` exercises both MCP tools without Claude Code. It was last verified with MCP Python SDK 2.3.0.

This folder is a git repository; commit content changes normally. Playwright and its browsers are not installed, so do not claim Playwright tests passed; the Playwright examples are syntax-checked only. The MCP demo was verified with its smoke test, but its dependencies live in `mcp-demo/.venv` or an ad-hoc `uv` environment, not the system Python.

## Relationship between the AI handbook and deck

The handbook is the source of truth; the deck is a much shorter workshop version of the same onboarding material. The deck's sections loosely follow the handbook: Understand → Part 1, Ask → Part 2, Operate → Part 3, Build → Parts 4–5, Apply → Parts 6–8. A substantive change to a concept, command, or figure should be reflected in both, with the deck staying condensed. The handbook is the reference readers keep; the deck is what a presenter walks a group through. Both must end with the reader able to start working with AI, not merely informed about it.
