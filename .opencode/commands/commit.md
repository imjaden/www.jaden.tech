---
description: Stage and commit changes with conventional commit message
---

Analyze the working tree changes and help commit them.

## Steps

1. Run `git status --short` and `git diff --stat` to understand what changed
2. Group changes by logical concern
3. For each group, generate a conventional commit message

## Commit format

```
type@scope: subject
```

### Types

| Type | When |
|------|------|
| `add` | New feature / file |
| `optimized` | Improvement (perf, structure, readability) |
| `fixed` | Bug fix |
| `remove` | Delete feature / file |
| `refactor` | Restructure without behavior change |
| `docs` | Documentation |
| `test` | Testing |
| `chore` | Build / tooling / deps |

### Rules

- English subject, verb-first (`add`, `fix`, `optimize`, `remove`)
- Describe effect, not implementation
- No period at end
- Group by logical concern — do NOT `git add -A` blindly
- Present the commit plan and ask for confirmation before executing
