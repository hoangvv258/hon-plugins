---
name: search-issues
description: Search for Jira issues using JQL queries
argument-hint: "[jql_query] - Optional JQL query string (e.g., 'project = PROJ AND status = \"To Do\"')"
allowed-tools: []
---

# Search Jira Issues

Search for Jira issues using Jira Query Language (JQL). You can filter by project, status, assignee, priority, and more.

## How to use

When the user asks to search for Jira issues, use this command to:

1. Ask the user for search criteria if not provided:
   - Project key (required)
   - Status filters (optional: To Do, In Progress, Done, etc.)
   - Assignee (optional: specific user or unassigned)
   - Priority (optional: Critical, High, Medium, Low)
   - Other filters (labels, components, due date, etc.)

2. Build the JQL query based on their criteria
3. Execute the search via Jira REST API: `GET /rest/api/3/search?jql=...&maxResults=50`
4. Parse and display the search results in a formatted table with:
   - Issue Key
   - Summary
   - Status
   - Priority
   - Assigned To
   - Due Date (if set)

## Implementation pseudo-code

```python
# Build JQL query dynamically
def build_jql_from_criteria(project, status, assignee, priority, labels):
    conditions = [f'project = {project}']
    
    if status:
        conditions.append(f'status IN ({",".join(status)})')
    
    if assignee:
        if assignee.lower() == "unassigned":
            conditions.append('assignee = EMPTY')
        else:
            conditions.append(f'assignee = {assignee}')
    
    if priority:
        conditions.append(f'priority IN ({",".join(priority)})')
    
    if labels:
        conditions.append(f'labels IN ({",".join(labels)})')
    
    jql = ' AND '.join(conditions)
    return jql

# Execute search
def search_issues(jql, max_results=50):
    response = client.get(
        "/rest/api/3/search",
        params={
            "jql": jql,
            "maxResults": max_results,
            "fields": "key,summary,status,priority,assignee,duedate,labels"
        }
    )
    
    data = response.json()
    return format_results_table(data["issues"])

# Format for display
def format_results_table(issues):
    rows = []
    for issue in issues:
        fields = issue["fields"]
        rows.append({
            "Key": issue["key"],
            "Summary": fields["summary"][:50],  # Truncate
            "Status": fields["status"]["name"],
            "Priority": fields["priority"]["name"],
            "Assignee": fields["assignee"]["displayName"] if fields.get("assignee") else "Unassigned",
            "Due": fields.get("duedate", "—")
        })
    return format_as_table(rows)
```

## Common search patterns

- `project = PROJ AND status = "To Do"` - All to-do items in a project
- `assignee = currentUser() AND status != Done` - My unfinished work
- `priority = High OR priority = Critical` - High priority issues
- `updated >= -7d` - Recently updated
- `duedate <= now()` - Overdue items

## Error handling

Handle common search errors:

```python
try:
    response = client.get("/rest/api/3/search", params={"jql": jql})
except httpx.HTTPStatusError as e:
    if e.response.status_code == 400:
        # Invalid JQL syntax
        print("Invalid search query. Check your JQL syntax.")
    elif e.response.status_code == 401:
        # Auth failed
        print("Authentication failed. Check your API token.")
    elif e.response.status_code == 429:
        # Rate limited
        print("Too many requests. Wait and try again.")
```

Reference `references/error-handling.md` for detailed error strategies.

## Tips

- Use the `jira-integration` skill for detailed JQL syntax examples
- For complex queries, ask the user to clarify filters rather than guessing
- Always show the JQL query being executed so users can refine it
- Paginate results if more than 10 issues found
- Let users refine the search with additional filters
- Validate JQL length (max 8000 characters)
