# Jira Assistant Plugin

Integrate Jira issue management directly into Claude Code. Create, search, update, and transition Jira issues without leaving your editor.

## Features

- **Create Issues**: Create Jira issues with customizable fields
- **Search Issues**: Find issues using JQL and interactive search
- **Update Issues**: Modify issue fields, status, and assignments
- **Comment**: Add comments and updates to issues
- **Transition**: Move issues through workflow statuses
- **Sprint Info**: View sprint and board information
- **Link to Code**: Associate issues with code files
- **Intelligent Analysis**: Get AI-powered suggestions for issue fixes and categorization

## Setup

### 1. Configure Jira Connection

Create a `.claude/jira-assistant.local.md` file in your project:

```markdown
---
jiraUrl: "https://yourcompany.atlassian.net"
apiToken: "your_api_token_here"
defaultProjectKey: "PROJ"
defaultAssignee: "username"
defaultIssueType: "Task"
---
```

**Required fields:**
- `jiraUrl`: Your Jira instance URL
- `apiToken`: Jira API token (generate at https://id.atlassian.com/manage-profile/security)

**Optional fields:**
- `defaultProjectKey`: Default project for new issues
- `defaultAssignee`: Default assignee for new issues
- `defaultIssueType`: Default issue type (Bug, Feature, Task, etc.)

### 2. Get Your API Token

1. Visit https://id.atlassian.com/manage-profile/security
2. Click "Create API token"
3. Copy the token
4. Add it to `.claude/jira-assistant.local.md` as `apiToken`

## Usage

### Commands

Use slash commands to interact with Jira:

- `/jira:search` - Search Jira issues
- `/jira:create` - Create a new Jira issue
- `/jira:update` - Update an existing issue
- `/jira:comment` - Add a comment to an issue
- `/jira:transition` - Transition an issue to a new status
- `/jira:sprint-info` - View sprint and board information
- `/jira:link-issue` - Link an issue to code files

### Agent

Ask Claude to analyze Jira issues:

> "Analyze the open issues in our PROJ project and suggest which ones could be fixed quickly"

The Jira analyzer will:
- Suggest solutions and fixes
- Categorize issues by type and priority
- Identify related or duplicate issues
- Extract actionable tasks

## Supported Jira Versions

- Jira Cloud (recommended)
- Jira Server 8.0+ (self-hosted)

## Troubleshooting

**"Authentication failed"**: Check that your API token is correct and not expired.

**"Project not found"**: Verify your project key in the settings.

**"API rate limit"**: Wait a few moments and try again.

## Contributing

Improvements and suggestions are welcome!

## License

MIT
