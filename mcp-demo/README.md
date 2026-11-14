# Flashcards MCP Demo

A minimal local MCP server that exposes two tools over SQLite:

- `search_cards(query, limit=5)` — search flashcards by question or answer.
- `add_card(question, answer, source="")` — add a flashcard and return its id.

It is the runnable example for [Part 4.5 of the AI handbook](../using-ai-from-zero-to-claude-code.md#45-hooks-mcp-and-plugins-a-quick-map). It needs no account, API key, or network access. The database is created on first run and seeded with three PSY 101 cards.

## Files

| File | Purpose |
|---|---|
| `server.py` | The MCP server. Exposes the two tools over stdio. |
| `smoke_test.py` | Exercises both tools without Claude Code. |
| `requirements.txt` | `mcp>=2,<3` |
| `cards.db` | Created on first run; ignored by Git. |

## Quick start

### 1. Install

```powershell
cd C:\Users\<you>\AI_Study\mcp-demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
cd ~/AI_Study/mcp-demo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Test without Claude Code

```bash
python smoke_test.py
```

You should see the tool names, a search hit for “confirmation bias,” the newly added “schema” card, and `Smoke test passed.`

### 3. Connect it to Claude Code

Use the absolute path to the Python interpreter that has `mcp` installed, and the absolute path to `server.py`:

```powershell
claude mcp add flashcards-db -- "C:\Users\<you>\AI_Study\mcp-demo\.venv\Scripts\python.exe" "C:\Users\<you>\AI_Study\mcp-demo\server.py"
```

macOS/Linux:

```bash
claude mcp add flashcards-db -- "/Users/<you>/AI_Study/mcp-demo/.venv/bin/python" "/Users/<you>/AI_Study/mcp-demo/server.py"
```

If you are not using a virtual environment, replace the interpreter path with `python` (Windows) or `python3` (macOS/Linux), and make sure `mcp` is installed for that interpreter.

Start a **new** Claude Code session in this folder, run `/mcp`, and confirm `flashcards-db` is connected. MCP servers load at session start.

### 4. Try it

```text
Use the flashcards-db MCP server to add a card:
Q: What is a schema?
A: A mental framework that organizes knowledge.
Source: Lecture 04
Then search for "schema" and show me the stored card.
```

Claude should call `add_card`, then `search_cards`, and show the new row. Search for `bias` to see the seeded cards.

### 5. Reset or remove

- Delete `cards.db` to reset the sample data.
- Remove the server from Claude Code:

```bash
claude mcp remove flashcards-db
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: mcp` | Install `requirements.txt` into the same interpreter used in the `claude mcp add` command. |
| Server shows as failed in `/mcp` | Check the interpreter and `server.py` paths; run `python smoke_test.py`; start a new session. |
| `cards.db` permission error | Run from a folder you can write to, or change `DB_PATH` in `server.py`. |
| Tool result is empty | Search for a seeded term such as `bias`, or add a card first. |

## Security notes

- The server is local, uses no credentials, and exposes only two operations on one SQLite file.
- Do not commit `cards.db` if it contains real study data; `.gitignore` already excludes it.
- Treat any MCP server as code with access. Read `server.py` before connecting it.

## Version

The demo uses the MCP Python SDK 2.x (`mcp.server.mcpserver.MCPServer`). In SDK 1.x the class was named `FastMCP`; older tutorials use that name.
