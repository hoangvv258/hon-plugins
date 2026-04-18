---
name: link-issue-to-code
description: Link a Jira issue to code files, pull requests, or commits
argument-hint: "[issue_key] [code_reference] - Issue key and file/PR/commit to link (interactive if not provided)"
allowed-tools: []
---

# Link Issue to Code

Associate a Jira issue with code changes, pull requests, or commits. This creates traceability between work tracking and actual code.

## How to use

When the user wants to link an issue to code:

1. **Get the issue key** (e.g., "PROJ-123")
2. **Get the code reference**:
   - File path in repository
   - Pull request URL/number
   - Commit hash
   - Branch name

3. **Create the link**:
   - Add issue key to branch name: `PROJ-123/feature-description`
   - Add issue key to commit message: "PROJ-123: Implement feature"
   - Add issue key to PR description
   - Add comment with link to code

4. **Show confirmation** of the link

## Link types

**1. Code File**:
- "Link PROJ-123 to src/auth/login.py"
- Purpose: Mark which files implement the feature

**2. Pull Request**:
- "Link PROJ-123 to PR #456"
- Purpose: Track which PR resolves the issue

**3. Commit**:
- "Link PROJ-123 to commit abc1234"
- Purpose: Document exact change

**4. Branch**:
- "Link PROJ-123 to feature/auth-refactor"
- Purpose: Track work in progress

## Best practices

### In commit messages:
```
PROJ-123: Refactor authentication system

- Extract auth logic to separate module
- Add unit tests
- Update documentation
```

### In branch names:
```
PROJ-123/auth-refactor
PROJ-456/fix-login-timeout
BUG-789/mobile-scroll-issue
```

### In PR descriptions:
```
## Resolves
- Closes #PROJ-123

## Description
This PR implements the authentication refactor tracked in PROJ-123.
```

## Interactive flow

```
You: Link PROJ-123 to the code
Bot: What type of code reference?
  1. File in repository
  2. Pull request
  3. Commit hash
  4. Branch name
Bot: File path? [e.g., src/auth/login.py]
Bot: Add note? [optional]
Bot: Link created! [confirmation]
```

## Tips

- Mention issue key early in branch/commit: "PROJ-123: ..." not "implement PROJ-123"
- Include issue keys in PR titles and descriptions for automated linking
- Use this to document traceability for audits
- Support bulk linking: "Link these 5 issues to PR #456"
- Create issue-to-PR mapping for release notes

## Integration with CI/CD

- Automate issue linking in CI/CD pipelines
- Automatically transition issues when PRs are merged
- Generate change logs from linked issues
- Track feature deployment from issue to production
