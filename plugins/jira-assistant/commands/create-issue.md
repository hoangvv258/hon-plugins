---
name: create-issue
description: Create a new Jira issue
argument-hint: "[project_key] [issue_type] [summary] - Issue details (interactive prompt if not provided)"
allowed-tools: []
---

# Create Jira Issue

Create a new issue in Jira with required and optional fields.

## How to use

When the user wants to create an issue:

1. **Gather required information** (ask if not provided):
   - Project key (e.g., "PROJ", use default from settings if available)
   - Issue type (Bug, Feature, Task, Epic, etc.)
   - Summary (issue title)

2. **Gather optional information** (ask in a conversational way):
   - Description (detailed explanation)
   - Assignee (who should work on it)
   - Priority (Critical, High, Medium, Low)
   - Labels (tags for categorization)
   - Components (which component this affects)
   - Due date (when it's due)

3. **Confirm the details** with the user before creating
4. **Create the issue** using the Jira API
5. **Display the result** with the new issue key and link

## Implementation pseudo-code

```python
# Build issue payload
def build_issue_payload(project, issue_type, summary, **kwargs):
    payload = {
        "fields": {
            "project": {"key": project},
            "summary": summary,
            "issuetype": {"name": issue_type}
        }
    }
    
    # Add optional fields
    if kwargs.get("description"):
        payload["fields"]["description"] = kwargs["description"]
    
    if kwargs.get("assignee"):
        payload["fields"]["assignee"] = {"name": kwargs["assignee"]}
    
    if kwargs.get("priority"):
        payload["fields"]["priority"] = {"name": kwargs["priority"]}
    
    if kwargs.get("labels"):
        payload["fields"]["labels"] = kwargs["labels"].split(",")
    
    if kwargs.get("due_date"):
        payload["fields"]["duedate"] = kwargs["due_date"]
    
    return payload

# Create issue
def create_issue(project, issue_type, summary, **kwargs):
    payload = build_issue_payload(project, issue_type, summary, **kwargs)
    
    response = client.post(
        "/rest/api/3/issues",
        json=payload
    )
    
    if response.status_code == 201:
        data = response.json()
        issue_key = data["key"]
        issue_id = data["id"]
        issue_url = f"{jira_url}/browse/{issue_key}"
        return {
            "key": issue_key,
            "id": issue_id,
            "url": issue_url,
            "message": f"✓ Created {issue_key}: {summary}"
        }
    else:
        return handle_error(response)
```

## Interactive flow

```
You: I need to create a new Jira issue
Bot: What project? [use default if set] 
Bot: What type? (Bug/Feature/Task/Epic)
Bot: What's the summary?
Bot: Add description? [optional]
Bot: Assign to anyone? [optional]
Bot: Set priority? [optional]
Bot: Create issue? [confirm]
-> Created: PROJ-123: New Feature Title
   Open in Jira: https://yourinstance.atlassian.net/browse/PROJ-123
```

## Error handling

Handle creation errors:

```python
try:
    response = client.post("/rest/api/3/issues", json=payload)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 400:
        # Invalid fields or missing required data
        error_data = e.response.json()
        print(f"Invalid data: {error_data['errors']}")
    elif e.response.status_code == 403:
        # Permission denied
        print("You don't have permission to create issues in this project")
    elif e.response.status_code == 404:
        # Project not found
        print("Project not found. Check the project key.")
```

Reference `references/error-handling.md` for detailed error strategies.

## Tips

- Start with the required fields, then offer optional fields
- Use the default project from settings if configured
- Allow bulk creation: "Create 3 bugs for..."
- Show the issue link so users can open it in Jira
- Ask clarifying questions if fields are vague
- Use `jira-integration` skill for issue type and field guidance
- Validate issue type exists in project before creating
- Use project metadata to get available issue types:
  ```
  GET /rest/api/3/projects/{projectKey}
  ```
