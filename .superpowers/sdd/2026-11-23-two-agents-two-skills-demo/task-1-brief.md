### Task 1: Create the folder and the article

**Files:**
- Create: `AI_general/two-agents-two-skills-demo/article.md`

**Interfaces:**
- Consumes: nothing.
- Produces: `article.md` — the shared source read by both agents (Tasks 4–5).

- [ ] **Step 1: Create the demo folder**

Run: `New-Item -ItemType Directory -Force "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo"`
Expected: directory exists.

- [ ] **Step 2: Write `article.md` with this exact content**

```markdown
# Why Leaves Change Color in Autumn

In spring and summer, leaves are green because they contain large amounts of
chlorophyll, the pigment that captures sunlight for photosynthesis. As days
shorten and temperatures fall, trees stop producing chlorophyll. The green
fades, and pigments that were hidden underneath — yellow carotenoids and
orange xanthophylls — become visible.

Some trees also make red anthocyanins in autumn, especially when sunny days
are followed by cool nights. These pigments may help protect the leaf while
it sends nutrients back into the tree.

Eventually the tree seals off each leaf at the stem, and the leaf falls. The
colors are not new: they were there all along, or appear briefly as the leaf
finishes its work.
```

- [ ] **Step 3: Verify the article**

Run: `(Get-Content "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\article.md" | Measure-Object -Word).Words`
Expected: a number between 100 and 160.

---

