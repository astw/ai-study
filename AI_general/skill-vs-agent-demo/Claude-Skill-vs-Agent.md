# Skill vs Agent: Where the Context Lives

Suppose the model has a 100M-token context window. What is the context size
when you load 3 skills, versus when you use 3 agents? The answer is not
100M ÷ 3.

## Short Answer

With **3 skills**, everything shares one conversation and one 100M window. Each
skill is just instructions added to that window, so all three skill bodies and
the whole conversation history compete for the same 100M.

With **3 agents**, each agent is a separate model invocation with its own fresh
context window. Each agent can use up to the full 100M on its own — the window
is not divided by 3. Total capacity is effectively 3 × 100M = 300M, while the
parent conversation grows only by the prompts it sends out and the reports it
gets back.

So the context size per agent is **up to 100M each**, not 100M / 3.

## The Two Shapes

### 3 skills, one conversation

- One context window for everything.
- Main context = conversation history + skill A + skill B + skill C.
- Every skill body competes for the same 100M budget.
- Anything any skill read stays available for follow-up questions in the same
  conversation.

### 3 agents, one parent

- Three independent invocations, each with its own context window.
- Each agent's context = its input prompt + whatever instructions it was given
  + the files it reads, capped at 100M per agent.
- The parent's context holds only the prompts sent out and the short reports
  that come back.
- Agents cannot see the parent's conversation, and they cannot see each other's
  work.

## Side by Side

| | 3 skills | 3 agents |
|---|---|---|
| Context windows | 1, shared | 3 independent + 1 parent |
| Capacity for the work | 1 × 100M, shared | up to 3 × 100M total |
| What the parent holds | every skill body and everything read | prompts sent + reports received |
| Follow-up about the source | answered from shared context | needs a re-read or re-delegation |
| Coordination | natural, same context | none, isolated workers |

## What This Demo Shows

The same contrast appears with this folder's single 121-word article:

- `/summarize-inline` runs in the main conversation. The article and its three
  bullets stay in context, so the follow-up "Which two pigment names does the
  article give for yellow and orange?" is answered directly from memory
  (Step 4 of `README.md`).
- The `summarizer` agent reads the same file in its own context. Only its three
  bullets return. Those bullets do not name the pigments, so the parent must
  read `article.md` itself or delegate again. That extra step is the
  demonstration (Step 7 of `README.md`).

In other words: with the agent, the parent saves the article's text — and in
exchange it loses the article's text.

## Trade-Offs

- **Isolation is capacity, but also amnesia.** An agent starts clean, which is
  why many agents can each use a full window. The price is that agents cannot
  ask you questions mid-task, cannot see the conversation, and cannot build on
  each other's work in one shared context.
- **You pay per context.** Every agent processes its own context separately,
  so the extra capacity is not free.
- **Coordination is manual.** Skills compose inside one conversation; agents
  must be orchestrated by the parent, which then merges their reports.

A 100M window is hypothetical — production model windows are much smaller
today — but the arithmetic and the architecture are the same at any size.
