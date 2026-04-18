# Jira Assistant Plugin Configuration Guide

## Plugin Architecture

The Jira Assistant plugin provides interactive commands, an intelligent agent, and skills for managing Jira issues directly from Claude Code.

### Component Overview

| Component | Type | Purpose | Tools |
|-----------|------|---------|-------|
| Skill | Knowledge | Jira API patterns, authentication, JQL reference | — |
| Commands (7) | Interactive | User-initiated issue operations | None (API calls via prompts) |
| Agent | Autonomous | Intelligent issue analysis | read, write, bash |

### Why Commands Have No Allowed Tools

Commands like `/jira:search-issue` are **interactive commands written FOR Claude** to execute, not **command handlers that execute tools**.

When Claude executes a command:
1. Claude reads the command markdown (instruction)
2. Claude interacts with the user to gather inputs
3. Claude makes Jira API calls using knowledge from the skill
4. Claude displays results to the user

The `allowed-tools: []` constraint means:
- ✅ Claude can use the `jira-integration` skill for guidance
- ✅ Claude can read environment/settings for credentials
- ❌ Claude cannot invoke arbitrary bash commands or file operations
- ❌ Claude cannot make unrestricted calls to external services

This **prevents security issues** while allowing full Jira integration via REST API knowledge.

## Settings Configuration

Store plugin settings in `.claude/jira-assistant.local.md`:

```markdown
---
jiraUrl: "https://yourinstance.atlassian.net"
apiToken: "your_api_token_here"
defaultProjectKey: "PROJ"
defaultAssignee: "john.doe"
defaultIssueType: "Task"
---
```

### Reading Settings in Commands

Commands extract settings from the YAML frontmatter:

```python
def load_settings():
    """Read settings from .claude/jira-assistant.local.md"""
    settings_file = ".claude/jira-assistant.local.md"
    with open(settings_file) as f:
        frontmatter = f.read().split("---")[1]
        return yaml.safe_load(frontmatter)

settings = load_settings()
jira_url = settings["jiraUrl"]
api_token = settings["apiToken"]
```

### Required Settings

**Must be set before any command works**:
- `jiraUrl`: Your Jira instance URL
- `apiToken`: API token from https://id.atlassian.com/manage-profile/security

**Optional settings** (commands prompt for these if not set):
- `defaultProjectKey`: Default project for new issues
- `defaultAssignee`: Default assignee
- `defaultIssueType`: Default issue type (Bug, Feature, Task)

## API Integration Pattern

All commands follow this pattern for API calls:

1. **Extract settings** from `.claude/jira-assistant.local.md`
2. **Build request** based on user input
3. **Call Jira API** with Basic Auth:
   ```
   Authorization: Basic base64(email:api_token)
   ```
4. **Handle errors** gracefully (see `skills/jira-integration/references/error-handling.md`)
5. **Display results** in formatted table

### Example: Search Command Flow

```
User: "Show me high priority bugs"
    ↓
Command reads settings (jiraUrl, apiToken)
    ↓
Command builds JQL: 'type = Bug AND priority = High'
    ↓
Command calls: GET /rest/api/3/search?jql=...
    ↓
Command formats and displays results
```

## Security Considerations

### Credentials

- ✅ Stored in `.claude/jira-assistant.local.md` (excluded by .gitignore)
- ✅ API tokens are personal (generated per user)
- ✅ Tokens can be revoked immediately if leaked
- ⚠️ Never commit credentials to version control
- ⚠️ Never share `.claude/jira-assistant.local.md` files

### Permissions

- Each API token has the same permissions as its user
- Plugin respects Jira's permission system
- Users can only create/update issues they have permission for
- Some operations may fail if user lacks project permissions

### Rate Limiting

Jira Cloud enforces **180 requests/minute per API token**:

```python
# Implement exponential backoff for 429 responses
if response.status_code == 429:
    retry_after = response.headers.get("Retry-After", "2")
    time.sleep(int(retry_after))
```

## Troubleshooting

### "Authentication failed"
- Check API token is valid: https://id.atlassian.com/manage-profile/security
- Verify email is correct
- Token must be generated, not password

### "Project not found"
- Verify project key is correct (e.g., "PROJ" not "Project")
- Check you have access to the project
- List available projects: `GET /rest/api/3/project`

### "Permission denied"
- Check your user has project access
- Some issue types may be restricted
- Ask Jira admin for permissions

### "Rate limited"
- Wait before retrying (429 response includes `Retry-After`)
- Batch operations where possible
- Implement caching for frequently accessed data

## Extending the Plugin

To add new commands:

1. **Create command file** in `commands/` directory (e.g., `clone-issue.md`)
2. **Reference the skill** for API guidance
3. **Follow the established pattern**:
   - Interactive user input
   - JQL/API call
   - Formatted output
   - Error handling

Example template:
```markdown
---
name: command-name
description: What this command does
argument-hint: "[arg1] [arg2] - Optional arguments"
allowed-tools: []
---

# Command Name

Description...

## How to use

Steps...

## Implementation

Pseudo-code...
```

## Supported Jira Versions

- ✅ **Jira Cloud** (recommended) - Fully supported with API v3
- ✅ **Jira Server 8.0+** (self-hosted) - Supported with API v2
- ❌ **Jira Server 7.x and earlier** - Not supported (use v2 API)

Note: Some field names and API endpoints may differ between versions. Consult `references/api-patterns.md` for version-specific patterns.

## Performance Tips

1. **Cache project metadata** (issue types, fields, statuses)
2. **Use JQL for filtering** instead of fetching all issues
3. **Limit search results** with `maxResults` parameter
4. **Batch operations** when creating/updating multiple issues
5. **Handle pagination** for large result sets

## Related Resources

- **Jira REST API**: https://docs.atlassian.com/software/jira/docs/api/rest/latest
- **JQL Tutorial**: https://support.atlassian.com/jira-cloud-platform/docs/learn-jql
- **API Token Generation**: https://id.atlassian.com/manage-profile/security
- **Jira Status Page**: https://status.atlassian.com
