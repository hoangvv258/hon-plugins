---
name: Jira Integration
description: This skill should be used when the user asks to "integrate Jira", "work with Jira API", "configure Jira authentication", "understand JQL queries", "Jira issue management", or mentions "Jira workflows". Provides comprehensive guidance on Jira REST API patterns, authentication, issue operations, and best practices for managing issues programmatically.
version: 0.1.0
---

# Jira Integration Guide

## Overview

Jira integration via REST API enables programmatic access to Jira instances for issue management, workflow automation, and project tracking. This guide covers authentication, core operations, and best practices for building Jira-integrated applications.

## Core Concepts

### Authentication

Jira Cloud uses API tokens for authentication. Each API request includes:
- Basic Auth header: `Authorization: Basic base64(email:api_token)`
- Headers: `Content-Type: application/json`

For self-hosted Jira, API tokens work similarly. Generate tokens in user profile settings.

### Key Resources

**Issues**: Individual tasks, bugs, or features
- Fields: summary, description, assignee, status, priority, issue type
- Transitions: Move between workflow statuses (To Do → In Progress → Done)
- Comments: Discussions and updates on issues

**Projects**: Collections of related issues
- Identified by project key (e.g., "PROJ", "BUG")
- Contain boards (Kanban/Scrum) and sprints

**Sprints**: Time-boxed iterations (Scrum boards)
- Contains planned issues for delivery
- Status: Not Started, Active, Closed

## Common Operations

### Search Issues (JQL)

Jira Query Language (JQL) enables sophisticated issue searches:

```
project = PROJ AND status = "To Do" AND priority = High
assignee = currentUser() AND resolved >= -7d
type = Bug AND created >= 2024-01-01
```

**Common fields**: `project`, `status`, `assignee`, `priority`, `type`, `created`, `updated`, `summary`

### Create Issue

Minimal creation requires:
- `project.key`: Project key (e.g., "PROJ")
- `issuetype.name`: Type (Bug, Feature, Task, etc.)
- `summary`: Issue title

Optional but common:
- `description`: Detailed description
- `assignee.name`: Assignee username
- `priority.name`: Priority (High, Medium, Low)

### Update Issue

Modify existing fields via `fields` object:
```json
{
  "fields": {
    "assignee": {"name": "username"},
    "status": {"name": "In Progress"},
    "description": "Updated description"
  }
}
```

### Transitions

Move issue through workflow statuses. First query available transitions, then apply:

```
GET /issue/{key}/transitions  # See available transitions
POST /issue/{key}/transitions # Apply transition with transition ID
```

## Authentication Setup

To integrate Jira:

1. **Generate API Token**
   - Visit: https://id.atlassian.com/manage-profile/security
   - Create new API token
   - Store securely

2. **Configure Base URL**
   - Jira Cloud: `https://yourinstance.atlassian.net`
   - Self-hosted: `https://your-jira-instance.com`

3. **Store Credentials**
   - Store in `.claude/jira-assistant.local.md` settings file
   - Never commit API tokens to version control

## Additional Resources

For detailed patterns, advanced techniques, and working examples, consult:
- **`references/authentication.md`** - Authentication patterns and security
- **`references/api-patterns.md`** - Common REST API patterns
- **`references/jql-queries.md`** - JQL query examples and syntax
- **`references/error-handling.md`** - Error handling and recovery strategies
- **`examples/auth_example.py`** - Python authentication code
- **`examples/search_example.py`** - Issue search implementation

## Best Practices

1. **Rate Limiting**: Respect API rate limits (180 requests/minute for Cloud)
2. **Error Handling**: Always handle connection errors and invalid credentials
3. **Caching**: Cache project keys and custom fields to reduce API calls
4. **Batch Operations**: Use bulk endpoints when performing multiple updates
5. **Pagination**: Handle large result sets with `startAt` and `maxResults`
