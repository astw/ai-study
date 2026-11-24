# Claude Code: Skill vs Agent

## Quick Summary

| Feature | Skill | Agent (subagent) |
|----------|---------|---------|
| What it is | Instructions: a `SKILL.md` playbook Claude loads and follows | A worker: a separate Claude instance with its own context, tools, and model |
| Purpose | Teach Claude how to perform a specific task | Give Claude an independent role and responsibility |
| Scope | Narrow and reusable | Broader and goal-oriented |
| Trigger | Auto-invoked when relevant, or you type `/skill-name` | Assigned work explicitly (by Claude or by you) |
| Context | Runs inside the main conversation | Runs in its own separate context window |
| Example | Code Review Skill | QA Agent |

## Rule of Thumb

**Skill = HOW to do something**

**Agent = WHO is responsible for doing it**

Or: **skill = "here's the procedure, follow it"**; **agent = "go do this and come back with a summary."**

## Where They Live

| | Skill | Agent |
|---|---|---|
| Project | `.claude/skills/<name>/SKILL.md` | `.claude/agents/<name>.md` |
| Personal | `~/.claude/skills/<name>/SKILL.md` | `~/.claude/agents/<name>.md` |
| Other | Plugin `skills/` folders; legacy `.claude/commands/<name>.md` still works (custom slash commands were merged into skills) | Managed settings; plugin `agents/`; `--agents` CLI JSON for one session |

A skill is a **directory** (`SKILL.md` plus optional scripts and reference files). An agent is a **single Markdown file** whose body becomes that subagent's system prompt.

Frontmatter casing differs — a common silent-misconfiguration trap:

- Skills: **kebab-case** (`disable-model-invocation`, `argument-hint`, `allowed-tools`)
- Agents: **camelCase** (`disallowedTools`, `maxTurns`, `permissionMode`)

## How Each Is Triggered

**Skill**
- Claude auto-invokes it when the task matches its `description`.
- You can invoke it explicitly with `/skill-name` (if user-invocable).
- `disable-model-invocation: true` makes it user-only; `user-invocable: false` makes it Claude-only.
- The description sits in context cheaply; the body loads only when the skill is used and then stays in the conversation.

**Agent**
- Claude delegates automatically based on the agent's `description`.
- You can ask in natural language ("use the code-reviewer subagent") or with `@agent-<name>`.
- The Agent tool selects it via `subagent_type`.
- A whole session can run as one agent: `claude --agent <name>`.

## Examples

### Skill

```md
# Code Review Skill

1. Look for bugs
2. Check readability
3. Analyze performance
4. Suggest fixes
```

### Agent

```md
# QA Agent

Responsibilities:
- Run regression testing
- Validate releases
- Verify bug fixes
```

## Multi-Agent Setup

```text
Release Manager Agent
    ├── Build Agent
    ├── QA Agent
    ├── API Test Agent
    └── Documentation Agent
```

Note: this org-chart picture is a useful mental model, but in Claude Code subagents are **workers**, not persistent roles. The main conversation is the orchestrator; it spawns agents, they work in isolation, and each returns a final report. Subagents cannot ask you questions mid-task (`AskUserQuestion` is removed), and they do not see your conversation history unless they are a *fork*.

Agents use Skills:

```text
QA Agent
 ├── Smoke Testing Skill
 ├── Regression Testing Skill
 ├── API Testing Skill
 └── SQL Validation Skill
```

This works in both directions:

- An agent can preload skills with the `skills:` frontmatter field (full content loads at startup, not just descriptions).
- A skill can run itself in a subagent with `context: fork`, optionally choosing the agent type with `agent:`.

## Practical Differences

| Aspect | Skill | Agent |
|---|---|---|
| Context cost | Adds instructions to the main conversation | Burns its own context; only the final report returns to yours |
| Tool permissions | `allowed-tools` is a **pre-approval for that turn**, not a restriction | `tools` is a **real allowlist**; `disallowedTools` removes tools first |
| Model | Can set `model`/`effort` for the turn or forked run | Can use a different model entirely |
| Talk to the user | Yes — it is part of the main conversation | No — returns a report; cannot ask questions mid-task |
| Output | Instructions now active in your conversation | A summary/final report |
| Best for | Procedures, checklists, conventions, domain knowledge, repeatable workflows | Large searches, parallel independent tasks, specialized reviewers, keeping the main context clean |

## When to Choose

- Does the main assistant need this knowledge **while it works in front of you**? → Skill.
- Is this a self-contained job where you only want the **result**? → Agent.
- Need several independent investigations at once, or a huge codebase sweep without flooding the main conversation? → Agents.

## Common Pitfalls

1. **Wrong frontmatter casing** (kebab-case vs camelCase) is silently ignored.
2. **Expecting an agent to remember your conversation** — it starts fresh unless forked.
3. **Expecting an agent to ask clarifying questions** — it can't; put the details in the delegation.
4. **Treating `allowed-tools` in a skill as a sandbox** — it's pre-approval, not restriction.
5. **Making a skill for everything** — if it's a big isolated job, an agent keeps your context clean.
6. **Confusing names**: "agent" also refers to the agent view (`claude agents`) for managing parallel sessions, and in the Agent SDK it means the program you build. This document uses "agent" to mean a Claude Code subagent.

## One-Line Heuristic

**Knowledge that should apply while Claude works in front of you → skill.**
**Work that should happen out of sight and come back summarized → agent.**

## Sources

- Skills: https://code.claude.com/docs/en/skills
- Subagents: https://code.claude.com/docs/en/sub-agents
- Agents overview: https://code.claude.com/docs/en/agents
- Workflows comparison: https://code.claude.com/docs/en/workflows
- Agent SDK overview: https://code.claude.com/docs/en/agent-sdk/overview
