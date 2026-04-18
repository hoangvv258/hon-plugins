---
name: fetch-sprint-info
description: Get information about sprint status and board details
argument-hint: "[project_key] [sprint_name_or_id] - Project and sprint details (interactive if not provided)"
allowed-tools: []
---

# Fetch Sprint/Board Information

Get detailed information about sprints, boards, and their current status.

## How to use

When the user wants to see sprint or board information:

1. **Get the project key** (use default from settings if available)
2. **Ask which sprint or board** to view
3. **Display sprint details**:
   - Sprint name and ID
   - Status (Not Started, Active, Closed)
   - Start/end dates
   - Goal (if set)
   - Capacity (story points or count)

4. **Show board overview**:
   - Active sprint (if any)
   - Issue distribution by status
   - Top blockers
   - Completion percentage

5. **Allow drilling into issues**:
   - Show issues in each column/status
   - Filter by assignee, type, priority

## Information to display

**Sprint Summary**:
```
Sprint 15: Milestone Release
Status: Active (5 days remaining)
Start: 2024-01-08 | End: 2024-01-19
Goal: Complete user authentication refactor
Issues: 12 total (3 done, 5 in progress, 4 to do)
Velocity: 28 / 32 story points
```

**Board Overview**:
```
Current Board: PROJ Board
To Do: 15 issues
In Progress: 8 issues (2 blocked)
In Review: 3 issues
Done: 22 issues
```

## Interactive flow

```
You: Show me sprint status
Bot: Which project? [use default]
Bot: Which sprint? (or "current")
Bot: Displaying Sprint 15...
[Shows sprint details and board state]
Bot: Drill into a status column? [optional]
```

## Tips

- Show the active sprint by default
- Highlight blockers or at-risk issues
- Show burndown progress if available
- Allow filtering: "Show me In Progress items"
- Support comparisons: "Compare Sprint 14 vs Sprint 15"
- Provide actionable insights: "3 items at risk of missing deadline"
- Use tabular format for board columns

## Advanced views

- Sprint burndown trend
- Velocity history
- Team capacity allocation
- Blocker analysis
