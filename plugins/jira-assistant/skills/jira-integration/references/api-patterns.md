# Jira REST API Patterns

## Base URLs

**Jira Cloud**:
```
https://yourinstance.atlassian.net/rest/api/3
```

**Jira Server/Data Center**:
```
https://your-jira-instance.com/jira/rest/api/2
```

Note: API version 3 (Cloud) and v2 (Server) have slight differences. This guide focuses on API v3 (Cloud).

## Common Response Patterns

### Issue Response Object

```json
{
  "expand": "changelog,changelog.histories",
  "id": "10000",
  "self": "https://yourinstance.atlassian.net/rest/api/3/issue/10000",
  "key": "PROJ-123",
  "fields": {
    "summary": "Fix login bug",
    "description": "Users report login fails on mobile",
    "status": {
      "self": "...",
      "description": "The issue is open and ready for the sprint to start",
      "iconUrl": "...",
      "name": "To Do",
      "id": "10001",
      "statusCategory": {
        "self": "...",
        "id": 2,
        "key": "new",
        "colorName": "blue-gray",
        "name": "To Do"
      }
    },
    "assignee": {
      "self": "...",
      "accountId": "5b10ac8d82e05b22cc7d4ef5",
      "emailAddress": "user@example.com",
      "displayName": "Alice Johnson"
    },
    "priority": {
      "self": "...",
      "iconUrl": "...",
      "name": "High",
      "id": "2"
    },
    "issuetype": {
      "self": "...",
      "id": "10001",
      "description": "A bug in the product",
      "iconUrl": "...",
      "name": "Bug",
      "subtask": false
    },
    "created": "2024-01-01T10:00:00.000+0000",
    "updated": "2024-01-15T14:30:00.000+0000"
  }
}
```

## GET: Search Issues

**Endpoint**: `GET /search`

**Query Parameters**:
- `jql`: JQL query string
- `maxResults`: Number of results (default 50, max 100)
- `startAt`: Pagination offset (default 0)
- `fields`: Comma-separated field names to include

**Example**:
```bash
GET /search?jql=project=PROJ+AND+status="To Do"&maxResults=20&startAt=0
```

**Response**:
```json
{
  "expand": "names,schema",
  "startAt": 0,
  "maxResults": 20,
  "total": 5,
  "issues": [
    { "key": "PROJ-1", "fields": { ... } },
    { "key": "PROJ-2", "fields": { ... } }
  ]
}
```

## POST: Create Issue

**Endpoint**: `POST /issues`

**Minimal Payload**:
```json
{
  "fields": {
    "project": { "key": "PROJ" },
    "summary": "Fix login bug",
    "issuetype": { "name": "Bug" }
  }
}
```

**Full Example**:
```json
{
  "fields": {
    "project": { "key": "PROJ" },
    "summary": "Implement dark mode",
    "description": "Users request dark mode for the UI",
    "issuetype": { "name": "Feature" },
    "priority": { "name": "Medium" },
    "assignee": { "name": "username" },
    "components": [{ "name": "Frontend" }],
    "labels": ["enhancement", "ui"]
  }
}
```

**Response**:
```json
{
  "id": "10000",
  "key": "PROJ-123",
  "self": "https://yourinstance.atlassian.net/rest/api/3/issue/10000"
}
```

## PUT: Update Issue

**Endpoint**: `PUT /issues/{key}`

**Payload**:
```json
{
  "fields": {
    "summary": "Updated summary",
    "description": "Updated description",
    "assignee": { "name": "new_assignee" },
    "priority": { "name": "High" }
  }
}
```

**Partial Update** (PATCH):
```
PATCH /issues/{key}
```

## POST: Transition Issue

**Step 1**: Get available transitions
```
GET /issues/{key}/transitions
```

Response:
```json
{
  "expand": "transitions",
  "transitions": [
    {
      "id": "11",
      "name": "In Progress",
      "to": { "self": "...", "description": "Work is in progress", "name": "In Progress", "id": "3" }
    },
    {
      "id": "21",
      "name": "Done",
      "to": { ... }
    }
  ]
}
```

**Step 2**: Apply transition
```
POST /issues/{key}/transitions

{
  "transition": {
    "id": "11"
  },
  "update": {
    "assignee": [{ "set": { "name": "username" } }]
  }
}
```

## POST: Add Comment

**Endpoint**: `POST /issues/{key}/comments`

**Payload**:
```json
{
  "body": {
    "version": 1,
    "type": "doc",
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "This is a comment"
          }
        ]
      }
    ]
  }
}
```

## GET: Issue Transitions

**Endpoint**: `GET /issues/{key}/transitions`

Lists all available workflow transitions for the issue.

## GET: Project Details

**Endpoint**: `GET /projects/{projectIdOrKey}`

Returns project metadata including issue types and fields.

## Pagination Best Practices

For large result sets, use pagination:

```python
def get_all_issues(jql, batch_size=50):
    issues = []
    start_at = 0
    
    while True:
        response = client.get(
            "/search",
            params={
                "jql": jql,
                "maxResults": batch_size,
                "startAt": start_at
            }
        )
        data = response.json()
        issues.extend(data["issues"])
        
        if len(data["issues"]) < batch_size:
            break
        start_at += batch_size
    
    return issues
```

## Error Response Format

```json
{
  "errorMessages": ["Error message here"],
  "errors": {
    "fieldName": "Error detail"
  }
}
```

## Field Expansion

Use the `expand` parameter to include additional fields:

```
GET /issues/PROJ-123?expand=changelog,changelog.histories
```

## Issue Type Lookup

Different projects may have different issue types. Query available types:

```
GET /projects/{key}/issuetypes
```

## Custom Fields

Jira instances may have custom fields. Query field metadata:

```
GET /fields
```

This returns all available fields including custom ones (prefixed with `customfield_`).
