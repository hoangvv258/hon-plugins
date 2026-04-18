# Jira Authentication Patterns

## REST API Authentication

### Basic Auth Headers

All Jira REST API requests require Basic Authentication:

```python
import base64
import httpx

email = "user@company.com"
api_token = "your_api_token_from_profile"

credentials = base64.b64encode(f"{email}:{api_token}".encode()).decode()
headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}
```

### Testing Authentication

Verify credentials by querying the current user:

```bash
curl -X GET \
  "https://yourinstance.atlassian.net/rest/api/3/myself" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json"
```

Response on success:
```json
{
  "self": "https://yourinstance.atlassian.net/rest/api/3/users/abc123",
  "accountId": "abc123",
  "name": "username",
  "emailAddress": "user@company.com"
}
```

## Generating API Tokens

### Jira Cloud

1. Visit: https://id.atlassian.com/manage-profile/security
2. Under "API tokens", click "Create API token"
3. Give it a descriptive label (e.g., "Claude Code Integration")
4. Copy the token immediately (won't be shown again)
5. Store securely in environment or settings file

### Self-Hosted Jira

1. Log in to your Jira instance
2. Click profile avatar → Settings
3. Under "API tokens", click "Create API token"
4. Follow the same process as Cloud

## Security Best Practices

### Do NOT:
- Commit API tokens to version control
- Log or print API tokens
- Share tokens in plain text
- Use personal API tokens in shared systems

### Do:
- Store tokens in environment variables or secure config files
- Use `.gitignore` to exclude credential files
- Rotate tokens periodically
- Create separate tokens for different applications
- Use the most restrictive permissions needed

## Storing Credentials Securely

### Option 1: Environment Variables

```bash
export JIRA_URL="https://yourinstance.atlassian.net"
export JIRA_EMAIL="user@company.com"
export JIRA_API_TOKEN="your_token_here"
```

Then read in code:
```python
import os
jira_url = os.getenv("JIRA_URL")
email = os.getenv("JIRA_EMAIL")
api_token = os.getenv("JIRA_API_TOKEN")
```

### Option 2: Plugin Settings File

Store in `.claude/jira-assistant.local.md`:

```markdown
---
jiraUrl: "https://yourinstance.atlassian.net"
apiEmail: "user@company.com"
apiToken: "your_token_here"
---
```

Add to `.gitignore`:
```
.claude/*.local.md
```

## Connection Pooling

For production systems, maintain a connection pool:

```python
import httpx

class JiraClient:
    def __init__(self, base_url, email, api_token):
        self.base_url = base_url
        self.client = httpx.Client(
            auth=(email, api_token),
            timeout=30.0
        )
    
    def search(self, jql):
        response = self.client.get(
            f"{self.base_url}/rest/api/3/search",
            params={"jql": jql, "maxResults": 50}
        )
        return response.json()
    
    def close(self):
        self.client.close()

# Usage
client = JiraClient(base_url, email, api_token)
try:
    results = client.search("project = PROJ")
finally:
    client.close()
```

## Error Handling

### Common Authentication Errors

**401 Unauthorized**: Invalid credentials
- Verify email and API token
- Check token hasn't expired
- Ensure base URL is correct

**403 Forbidden**: Valid auth but insufficient permissions
- Check user has project permissions
- Verify API token scope

**429 Too Many Requests**: Rate limit exceeded
- Implement exponential backoff
- Cache results when possible
- Respect rate limit headers

### Retry Strategy

```python
import time
from httpx import HTTPStatusError

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except HTTPStatusError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")
```
