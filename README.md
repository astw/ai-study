# From Zero to Claude Code

A practical introduction to working with AI, written for people who have never used Claude Code. Read it with a laptop open; by the end you should be able to run a real Claude Code session and finish most of your work with it.

## What's in this folder

| File / folder | What it is | How to use it |
|---|---|---|
| `using-ai-from-zero-to-claude-code.md` | The handbook: 8 parts plus appendices A–F, with step-by-step instructions and exercises. | Read it in order. This is the main deliverable. |
| `ai-claude-code-slides-standalone.html` | The 40-slide workshop deck as a complete, self-contained web page. | Double-click to open in any browser. No server or install needed. |
| `ai-claude-code-slides.html` | The same deck as an Artifact fragment (no `<html>`/`<head>` wrapper), kept in sync for web publishing. | Use the standalone file for local viewing. |
| `mcp-demo/` | A runnable local MCP server over SQLite, with a smoke test and setup README. | Follow `mcp-demo/README.md`; no account or API key needed. |

## Who it's for

Complete beginners — the handbook specifically addresses college students — with no prior coding or terminal experience. No prior programming knowledge or special vocabulary is assumed; every technical idea is introduced when it is first needed. By the time you install Claude Code in Part 3, you will need a paid Claude plan (Pro, Max, Ultra, Team, or Enterprise) or a Console account; the free claude.ai plan does not include Claude Code.

## What you will learn

- What large language models are, what they are good at, and where they fail
- How to write prompts that produce usable first drafts instead of generic text
- How to install and use Claude Code: its interface, commands, and context management
- How to give Claude a memory with `CLAUDE.md`, and how permissions keep you in control
- How to turn repeated work into slash commands, skills, and subagents
- How to connect Claude Code to an external tool with a small local MCP server
- How Superpowers, OpenSpec, and RAG fit into larger projects — including a complete OpenSpec 2.0 walkthrough that adds cloze-deletion cards to the flashcards project
- How to apply all of this to studying, research, writing, coding, and daily admin

## How to use it

1. **Read the handbook from the beginning.** Parts 3–6 build one small project, adding one technique per part; skipping the exercises turns the rest into trivia.
2. **Keep Appendix A nearby.** It is the cheat sheet for launching Claude Code, in-session commands, prefixes, keybindings, and permission modes. Appendix B is a prompt library, Appendix C holds copy-paste file templates.
3. **Use the deck for a live session.** It is a condensed version of the same material, with speaker notes for whoever presents.
4. **Do the running project.** You play Maya, a first-year student turning lecture notes into a flashcard study tool. The project is a teaching example — the `flashcards/` files are not included in this folder; you build them as you read.

## Viewing the slide deck

Open `ai-claude-code-slides-standalone.html` directly in a browser. The deck also works as a published web page from `ai-claude-code-slides.html`.

Keyboard controls:

| Key | Action |
|---|---|
| `→` / `PageDown` / `Space` | Next slide |
| `←` / `PageUp` / `Shift+Space` | Previous slide |
| `Home` / `End` | First / last slide |
| `N` | Speaker notes |
| `O` | Contents overview |
| `Esc` | Close notes or overview |

## Other study guides

- [`tcp-ip-for-qa.md`](tcp-ip-for-qa.md) — a beginner-friendly TCP/IP, DNS, DHCP, and VPN primer for QA work, with a network test matrix, a diagnostic ladder, hands-on labs, and a bug-report template.
- [`playwright-for-qa.md`](playwright-for-qa.md) — a beginner-friendly Playwright for Python guide that tests the flashcards project from the AI handbook, with locators, assertions, fixtures, page objects, network mocking, debugging, CI, and labs.

## Version

Handbook Version 1.0 · November 2026. Claude Code and third-party tool details — including OpenSpec 2.0 and Superpowers 7.x — reflect that period; if something has changed, check the current upstream documentation before relying on it.
