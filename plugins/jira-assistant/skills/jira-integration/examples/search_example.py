#!/usr/bin/env python3
"""
Jira Search Examples

Demonstrates various search patterns using JQL.
"""

import base64

try:
    import httpx
except ImportError:
    import subprocess

    subprocess.check_call(["pip", "install", "httpx"])
    import httpx


def search_jira(jira_url: str, email: str, api_token: str, jql: str) -> dict:
    """Execute a JQL search against Jira."""
    credentials = base64.b64encode(f"{email}:{api_token}".encode()).decode()

    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json",
    }

    api_url = f"{jira_url.rstrip('/')}/rest/api/3"

    with httpx.Client(headers=headers) as client:
        response = client.get(
            f"{api_url}/search",
            params={
                "jql": jql,
                "maxResults": 20,
                "fields": "key,summary,status,assignee,priority,issuetype",
            },
        )
        response.raise_for_status()
        return response.json()


# Example JQL queries

EXAMPLES = {
    "Unfinished work": 'status != Done ORDER BY priority DESC',
    "My assigned issues": 'assignee = currentUser() AND status != Done',
    "High priority bugs": 'type = Bug AND priority = High AND status = "To Do"',
    "Recently updated": 'updated >= -7d ORDER BY updated DESC',
    "Due this week": 'duedate >= -7d AND duedate <= now()',
    "Unassigned issues": 'assignee = EMPTY AND status != Done',
    "Sprint planning": 'sprint = SPRINT-1 AND status IN ("To Do", "In Progress")',
    "Release candidates": 'fixVersion = "2.0" AND status != Done',
}


def print_results(data: dict):
    """Pretty print search results."""
    print(f"\nTotal: {data['total']} issues (showing {len(data['issues'])})\n")

    for issue in data["issues"]:
        key = issue["key"]
        fields = issue["fields"]
        summary = fields["summary"]
        status = fields["status"]["name"]
        priority = fields["priority"]["name"]
        issue_type = fields["issuetype"]["name"]
        assignee = (
            fields["assignee"]["displayName"]
            if fields.get("assignee")
            else "Unassigned"
        )

        print(f"{key}: {summary}")
        print(f"  Type: {issue_type} | Status: {status} | Priority: {priority}")
        print(f"  Assigned to: {assignee}\n")


def main():
    """Run example searches."""
    # Configuration
    JIRA_URL = "https://yourinstance.atlassian.net"
    EMAIL = "user@example.com"
    API_TOKEN = "your_token"
    PROJECT = "PROJ"

    print("Jira Search Examples")
    print("=" * 50)
    print("Update JIRA_URL, EMAIL, API_TOKEN, and PROJECT in the script")
    print()

    # Example 1: Your assigned issues
    print("Example 1: Issues assigned to you")
    print("-" * 50)
    jql1 = f'project = {PROJECT} AND assignee = currentUser() AND status != Done'
    print(f"JQL: {jql1}")
    # data1 = search_jira(JIRA_URL, EMAIL, API_TOKEN, jql1)
    # print_results(data1)

    # Example 2: Team's high priority work
    print("\nExample 2: High priority bugs needing work")
    print("-" * 50)
    jql2 = (
        f'project = {PROJECT} AND type = Bug '
        f'AND priority >= High AND status IN ("To Do", "In Progress")'
    )
    print(f"JQL: {jql2}")
    # data2 = search_jira(JIRA_URL, EMAIL, API_TOKEN, jql2)
    # print_results(data2)

    # Example 3: Stale issues
    print("\nExample 3: Issues not updated in 30 days")
    print("-" * 50)
    jql3 = f'project = {PROJECT} AND updated < -30d AND status != Done'
    print(f"JQL: {jql3}")
    # data3 = search_jira(JIRA_URL, EMAIL, API_TOKEN, jql3)
    # print_results(data3)

    # Example 4: Sprint readiness
    print("\nExample 4: Current sprint items not in progress")
    print("-" * 50)
    jql4 = f'project = {PROJECT} AND sprint = "Sprint 15" AND status != "In Progress"'
    print(f"JQL: {jql4}")
    # data4 = search_jira(JIRA_URL, EMAIL, API_TOKEN, jql4)
    # print_results(data4)

    # Example 5: Complex query
    print("\nExample 5: Critical path - high priority, unassigned")
    print("-" * 50)
    jql5 = (
        f'project = {PROJECT} AND '
        f'priority IN (Critical, High) AND '
        f'status IN ("To Do", "In Progress") AND '
        f'assignee = EMPTY'
    )
    print(f"JQL: {jql5}")
    # data5 = search_jira(JIRA_URL, EMAIL, API_TOKEN, jql5)
    # print_results(data5)

    print("\n" + "=" * 50)
    print("To run these examples:")
    print("1. Set JIRA_URL, EMAIL, API_TOKEN in this script")
    print("2. Uncomment the search_jira() and print_results() calls")
    print("3. Run: python search_example.py")


if __name__ == "__main__":
    main()
