# Jira API Error Handling

Handle common Jira API errors gracefully. This guide covers error patterns and recovery strategies.

## HTTP Status Codes

### 400 Bad Request
**Cause**: Invalid request parameters or malformed JSON

```python
try:
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    if e.response.status_code == 400:
        error_details = e.response.json()
        errors = error_details.get("errors", {})
        messages = error_details.get("errorMessages", [])
        print(f"Invalid request: {messages}")
        print(f"Field errors: {errors}")
```

**Fix**: Validate input before sending (especially JQL, field names)

### 401 Unauthorized
**Cause**: Invalid or expired API token

```python
if e.response.status_code == 401:
    print("❌ Authentication failed")
    print("   - Check API token is still valid")
    print("   - Regenerate at: https://id.atlassian.com/manage-profile/security")
    print("   - Update .claude/jira-assistant.local.md")
```

**Action**: Request new API token from user

### 403 Forbidden
**Cause**: Valid auth but insufficient permissions

```python
if e.response.status_code == 403:
    print("❌ Permission denied")
    print(f"   - User lacks permission for this action")
    print(f"   - Contact Jira admin or project lead")
    print(f"   - Error: {error_details.get('errorMessages', [])}")
```

### 404 Not Found
**Cause**: Issue, project, or resource doesn't exist

```python
if e.response.status_code == 404:
    error_msg = e.response.json().get("errorMessages", [])
    if "not found" in str(error_msg).lower():
        print(f"❌ Resource not found")
        print(f"   - Verify issue key: {issue_key}")
        print(f"   - Check project exists: {project_key}")
```

### 429 Too Many Requests
**Cause**: Rate limit exceeded (180 req/min for Jira Cloud)

```python
def retry_with_exponential_backoff(func, max_retries=3):
    """Retry with exponential backoff for rate limits."""
    for attempt in range(max_retries):
        try:
            return func()
        except httpx.HTTPStatusError as e:
            if e.response.status_code != 429:
                raise
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                retry_after = e.response.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after)
                
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

    raise Exception(f"Failed after {max_retries} retries")
```

### 500 Internal Server Error
**Cause**: Jira server error (rare)

```python
if e.response.status_code >= 500:
    print("❌ Jira server error")
    print(f"   - Status: {e.response.status_code}")
    print(f"   - Try again in a moment")
    print(f"   - Persistent? Check: https://status.atlassian.com")
```

## Common Business Logic Errors

### Invalid Transition
**Error**: "You cannot perform the action you've specified on this issue"

**Cause**: Issue cannot transition to target status (wrong current status or no permission)

```python
response = client.get(f"/issues/{key}/transitions")
available = [t["name"] for t in response.json()["transitions"]]
print(f"Valid transitions from current status: {available}")
```

**Fix**: Show user available transitions from current status

### Missing Required Field
**Error**: "Field 'priority' is required"

**Cause**: Issue type requires field that wasn't provided

```python
project = client.get(f"/projects/{project_key}")
issue_types = project["issueTypes"]
required_fields = issue_types[issue_type]["fields"]
```

**Fix**: Query available fields for issue type, show required ones to user

### Custom Field Not Found
**Error**: Field with ID 'customfield_10001' not found

**Cause**: Custom field doesn't exist or different Jira instance

```python
fields_response = client.get("/fields")
custom_fields = {f["id"]: f["name"] for f in fields_response if f["id"].startswith("customfield")}
```

**Fix**: Query available fields dynamically instead of hardcoding IDs

## Connection Error Handling

### Timeout
```python
try:
    response = client.get(url, timeout=30.0)
except httpx.TimeoutException:
    print("❌ Request timed out")
    print("   - Check network connection")
    print("   - Jira instance may be slow")
    print("   - Try again later")
```

### Connection Refused
```python
try:
    response = client.get(url)
except httpx.ConnectError:
    print("❌ Cannot connect to Jira instance")
    print(f"   - Check URL: {jira_url}")
    print(f"   - Check network/VPN connection")
    print(f"   - Is Jira instance up?")
```

## Validation Best Practices

### Pre-validation
```python
def validate_issue_key(key):
    """Validate issue key format."""
    if not key or '-' not in key:
        raise ValueError(f"Invalid issue key: {key}")
    proj, num = key.split('-')
    if not proj.isalpha() or not num.isdigit():
        raise ValueError(f"Invalid issue key format: {key}")

def validate_jql(jql):
    """Validate JQL before sending."""
    if not jql or len(jql) > 8000:
        raise ValueError("Invalid JQL query")
    # Could add JQL syntax validation here
```

### Post-response Validation
```python
def validate_response(response):
    """Validate response contains expected fields."""
    data = response.json()
    if "issues" not in data:
        raise ValueError("Unexpected API response format")
    return data
```

## User-Friendly Error Messages

Convert technical errors to user-friendly guidance:

```python
ERROR_MESSAGES = {
    400: "Invalid request. Check your input and try again.",
    401: "Authentication failed. Verify your API token and try again.",
    403: "You don't have permission for this action.",
    404: "Issue or project not found. Check the key and try again.",
    429: "Too many requests. Wait a moment and try again.",
    500: "Jira server error. Try again in a few moments.",
}

def get_user_message(status_code):
    return ERROR_MESSAGES.get(status_code, "An error occurred. Try again later.")
```

## Logging for Debugging

```python
import logging

logger = logging.getLogger("jira_assistant")
logger.setLevel(logging.DEBUG)

# Log API calls
logger.debug(f"GET {url}")
logger.debug(f"Status: {response.status_code}")
logger.debug(f"Response: {response.json()}")

# Log errors with full context
logger.error(f"API Error: {status_code}", extra={
    "url": url,
    "method": method,
    "response": response.text,
    "request": request_body
})
```
