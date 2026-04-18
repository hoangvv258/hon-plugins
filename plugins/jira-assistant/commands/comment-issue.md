---
name: comment-issue
description: Add a comment to a Jira issue
argument-hint: "[issue_key] [comment_text] - Issue key and comment (interactive if not provided)"
allowed-tools: []
---

# Comment on Jira Issue

Add a comment or update to an existing Jira issue to discuss progress, ask questions, or provide status updates.

## How to use

When the user wants to comment on an issue:

1. **Get the issue key** (e.g., "PROJ-123")
2. **Get the comment text** from the user
3. **Show preview** of the comment
4. **Confirm before posting**
5. **Post the comment** via Jira API
6. **Show confirmation** with timestamp

## Comment types

- **Status update**: "Started working on this"
- **Question**: "Can you clarify the requirements?"
- **Technical note**: "Found root cause in LoginController.java"
- **Review comment**: "Looks good, just needs..."
- **Block notification**: "Waiting on PROJ-456 to complete"

## Interactive flow

```
You: Comment on PROJ-123 that I started working on it
Bot: What's your comment?
Bot: Preview: "Started working on this"
Bot: Post comment? [confirm]
-> Comment added at 2024-01-15 10:30 UTC
```

## Tips

- Keep comments professional and clear
- Reference other issues using their keys (PROJ-789)
- Mention team members to notify them
- Use comments for status updates instead of changing status when still in progress
- Consider if this should trigger a status transition instead
- Use `@mention` syntax if supported for notifications

## Linking issues in comments

- Reference other issues: "This is blocked by PROJ-456"
- Cross-project references: "Related to DEPLOY-123"
- Commit references: "Fixed by commit abc1234"
