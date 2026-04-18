---
name: update-issue
description: Update an existing Jira issue's fields
argument-hint: "[issue_key] [field] [value] - Issue key and field to update (interactive if not provided)"
allowed-tools: []
---

# Update Jira Issue

Modify fields on an existing Jira issue.

## How to use

When the user wants to update an issue:

1. **Get the issue key** (e.g., "PROJ-123"):
   - Ask if not provided
   - Optionally search for it first if user describes it

2. **Determine what to update**:
   - Summary/Title
   - Description
   - Assignee
   - Priority
   - Status (use transitions if changing workflow status)
   - Labels
   - Components
   - Due Date
   - Any other field

3. **Get the new value** from the user
4. **Confirm changes** before applying
5. **Apply the update** via Jira API
6. **Show the result** with updated values

## Common update patterns

- **Reassign**: "Update PROJ-123, assign to john"
- **Change priority**: "Make PROJ-456 High priority"
- **Add labels**: "Tag PROJ-789 with 'urgent' and 'blocking'"
- **Bulk updates**: "Update these 5 issues to In Progress"
- **Update description**: "Change PROJ-111's description to..."

## Interactive flow

```
You: Update PROJ-123
Bot: What would you like to change?
Bot: Current assignee: Unassigned
Bot: New assignee? [option to keep or change]
Bot: Current priority: Medium
Bot: New priority? [ask or confirm]
Bot: Apply updates? [confirm]
-> Updated PROJ-123
```

## Important notes

- For status/workflow changes, use the `/jira:transition-issue` command instead
- Show current values before asking for new ones
- Allow multiple field updates in one command
- Use the `jira-integration` skill for field and value guidance
- Handle custom fields appropriately
