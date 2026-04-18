# JQL (Jira Query Language) Reference

JQL is Jira's query language for searching issues. All searches use the `/rest/api/3/search?jql=` endpoint.

## Basic Syntax

**Simple equality**:
```
project = PROJ
status = "To Do"
assignee = john
```

**AND/OR operators**:
```
project = PROJ AND status = "To Do"
priority = High OR priority = Critical
```

**Parentheses for grouping**:
```
(project = PROJ OR project = BUG) AND status = "In Progress"
```

**NOT operator**:
```
status != Done
assignee != EMPTY
```

## Common Fields

| Field | Values | Example |
|-------|--------|---------|
| `project` | Project key | `project = PROJ` |
| `status` | Status name | `status = "To Do"` |
| `assignee` | Username | `assignee = john` |
| `reporter` | Username | `reporter = jane` |
| `priority` | Highest, High, Medium, Low, Lowest | `priority = High` |
| `type` | Bug, Feature, Task, Epic, Subtask | `type = Bug` |
| `created` | Date | `created >= 2024-01-01` |
| `updated` | Date | `updated >= -7d` |
| `summary` | Text | `summary ~ "login"` |
| `description` | Text | `description ~ "bug"` |
| `label` | Label name | `labels = "urgent"` |
| `component` | Component name | `component = "Frontend"` |
| `sprint` | Sprint name or ID | `sprint = "Sprint 1"` |
| `duedate` | Date | `duedate <= 2024-02-01` |
| `fixVersion` | Version | `fixVersion = "1.0"` |

## String Matching

**Exact match** (case-insensitive):
```
summary = "Fix login bug"
```

**Contains** (~):
```
summary ~ "login"
description ~ "bug"
```

**Does NOT contain** (!~):
```
summary !~ "wontfix"
```

## Special Values

**Empty/Null**:
```
assignee = EMPTY
assignee = NULL
```

**Not empty**:
```
assignee != EMPTY
```

**Current user**:
```
assignee = currentUser()
reporter = currentUser()
```

## Date Operations

**Exact date**:
```
created = 2024-01-15
```

**Date ranges**:
```
created >= 2024-01-01 AND created < 2024-02-01
```

**Relative dates**:
- `-1d`: 1 day ago
- `-7d`: 7 days ago
- `-4w`: 4 weeks ago
- `-3m`: 3 months ago

**Examples**:
```
created >= -7d              # Last 7 days
updated >= -1d              # Updated in last day
duedate <= 2024-02-01       # Due by Feb 1
duedate >= -3d              # Due within 3 days
```

## Text Search Functions

**Case-sensitive exact**:
```
summary = "URGENT: Fix login"
```

**Contains substring**:
```
summary ~ "login"
```

**Regex pattern**:
```
summary ~ "fix.*login|login.*bug"
```

## Complex Examples

### Issues Assigned to Me

```
assignee = currentUser() AND status != Done
```

### High-Priority Bugs Assigned to Team

```
type = Bug AND priority >= High AND assignee IN (john, jane, bob)
```

### Issues Due This Sprint

```
sprint = "Sprint 15" AND status != Done
```

### Recently Updated Not Done

```
updated >= -3d AND status != Done AND project = PROJ
```

### Unassigned High-Priority Issues

```
assignee = EMPTY AND priority = High AND type != Epic
```

### Issues Created This Month

```
created >= -30d AND created < now() AND project = PROJ
```

### Complex Priority Query

```
(priority = Critical OR (priority = High AND assignee = EMPTY)) AND status IN ("To Do", "In Progress")
```

## Date Formatting

Dates can be specified as:
- `YYYY-MM-DD`: `2024-01-15`
- Relative: `now()`, `-7d`, `-4w`, `-3m`

## IN Operator

Select multiple values:
```
status IN ("To Do", "In Progress")
assignee IN (john, jane, bob)
priority IN (High, Critical)
```

## Sorting Results

Add ORDER BY to JQL queries:

```
project = PROJ ORDER BY created DESC
status = "To Do" ORDER BY priority DESC, duedate ASC
```

**Sort fields**: `created`, `updated`, `duedate`, `priority`, `assignee`, `summary`
**Order**: `ASC` (ascending), `DESC` (descending)

## Query Limits

- **Maximum query length**: 8000 characters
- **Maximum results**: 1000 (use pagination)
- **Default results**: 50

Use pagination parameters:
```
GET /search?jql=...&maxResults=100&startAt=0
```

## Common JQL Patterns

### Sprint Planning
```
sprint = SPRINT-1 AND status IN ("To Do", "In Progress")
```

### Backlog Review
```
sprint is EMPTY AND type != Epic ORDER BY priority DESC
```

### Quality Assurance
```
status = "Testing" AND assignee != EMPTY
```

### Release Readiness
```
fixVersion = "2.0" AND status != Done
```

### Performance Investigation
```
labels = "performance" OR summary ~ "slow|lag|timeout"
```

### Documentation Debt
```
labels = "documentation" AND assignee = EMPTY AND priority <= Medium
```
