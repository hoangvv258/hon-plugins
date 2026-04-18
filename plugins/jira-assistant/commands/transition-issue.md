---
name: transition-issue
description: Move a Jira issue to a different workflow status
argument-hint: "[issue_key] [target_status] - Issue key and new status (interactive if not provided)"
allowed-tools: []
---

# Transition Jira Issue

Move an issue through your workflow by transitioning it to a new status.

## How to use

When the user wants to change an issue's status:

1. **Get the issue key** (e.g., "PROJ-123")
2. **Show current status**
3. **Get available transitions** from Jira (only valid transitions shown)
4. **Ask which status to move to**
5. **Optionally update other fields** during transition (assignee, etc.)
6. **Confirm the transition**
7. **Apply the transition** via Jira API
8. **Show the new status**

## Common workflow transitions

**Typical workflow**: To Do → In Progress → In Review → Done

**Variations**:
- To Do → In Progress (start work)
- In Progress → In Review (ready for review)
- In Review → Done (approved)
- Any status → To Do (reopen)
- To Do → Won't Do (reject)

## Interactive flow

```
You: Mark PROJ-123 as in progress
Bot: Current status: To Do
Bot: Available transitions:
  1. In Progress (start work)
  2. Won't Do (skip this)
Bot: Which transition? [select In Progress]
Bot: Assign to you? [optional]
Bot: Apply transition? [confirm]
-> PROJ-123 is now In Progress
```

## Tips

- Show only valid transitions available from current status
- Allow optional field updates during transition (common: reassign during "In Progress")
- Let users add comments when transitioning
- Some statuses may have required fields before transitioning
- Use `jira-integration` skill for workflow configuration understanding
- Check if issue is already in target status to avoid unnecessary calls

## Bulk transitions

Support bulk operations:
- "Mark these 5 issues as done"
- "Move PROJ-111, PROJ-222, PROJ-333 to In Review"
