#!/usr/bin/env python3
"""
Jira Authentication Example

Demonstrates how to authenticate with Jira Cloud REST API and make basic requests.
"""

import base64
import json
import os
from typing import Optional

try:
    import httpx
except ImportError:
    print("Installing httpx...")
    import subprocess
    subprocess.check_call(["pip", "install", "httpx"])
    import httpx


class JiraClient:
    """Simple Jira REST API client with authentication."""

    def __init__(
        self,
        jira_url: str,
        email: str,
        api_token: str,
        timeout: float = 30.0,
    ):
        """
        Initialize Jira client.

        Args:
            jira_url: Base Jira URL (e.g., https://yourinstance.atlassian.net)
            email: Jira user email
            api_token: API token from profile settings
            timeout: Request timeout in seconds
        """
        self.jira_url = jira_url.rstrip("/")
        self.api_url = f"{self.jira_url}/rest/api/3"

        # Create Basic Auth header
        credentials = base64.b64encode(
            f"{email}:{api_token}".encode()
        ).decode()

        self.headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self.client = httpx.Client(timeout=timeout, headers=self.headers)

    def verify_authentication(self) -> bool:
        """Verify that authentication is working."""
        try:
            response = self.client.get(f"{self.api_url}/myself")
            response.raise_for_status()
            user = response.json()
            print(f"✓ Authenticated as: {user.get('displayName')}")
            print(f"  Email: {user.get('emailAddress')}")
            return True
        except httpx.HTTPError as e:
            print(f"✗ Authentication failed: {e}")
            return False

    def get_projects(self) -> list:
        """Get list of accessible projects."""
        try:
            response = self.client.get(f"{self.api_url}/project")
            response.raise_for_status()
            projects = response.json()
            print(f"\nAccessible projects ({len(projects)}):")
            for project in projects:
                print(f"  - {project['key']}: {project['name']}")
            return projects
        except httpx.HTTPError as e:
            print(f"Failed to get projects: {e}")
            return []

    def search_issues(self, jql: str, max_results: int = 10) -> list:
        """Search for issues using JQL."""
        try:
            response = self.client.get(
                f"{self.api_url}/search",
                params={
                    "jql": jql,
                    "maxResults": max_results,
                    "fields": "key,summary,status,assignee,priority",
                },
            )
            response.raise_for_status()
            data = response.json()
            print(f"\nFound {data['total']} issues:")
            for issue in data["issues"]:
                fields = issue["fields"]
                print(f"  - {issue['key']}: {fields['summary']}")
                print(
                    f"    Status: {fields['status']['name']}, "
                    f"Priority: {fields['priority']['name']}"
                )
            return data["issues"]
        except httpx.HTTPError as e:
            print(f"Search failed: {e}")
            return []

    def close(self):
        """Close the HTTP client."""
        self.client.close()


def main():
    """Example usage."""
    # Load credentials from environment or config
    jira_url = os.getenv("JIRA_URL", "https://yourinstance.atlassian.net")
    email = os.getenv("JIRA_EMAIL", "user@example.com")
    api_token = os.getenv("JIRA_API_TOKEN", "your_token_here")

    print("Jira REST API Authentication Example")
    print("=" * 40)

    if not api_token or api_token == "your_token_here":
        print("Error: Set JIRA_URL, JIRA_EMAIL, and JIRA_API_TOKEN environment variables")
        return

    # Create client
    client = JiraClient(jira_url, email, api_token)

    try:
        # Verify authentication
        if not client.verify_authentication():
            return

        # Get projects
        client.get_projects()

        # Search issues
        jql = 'project = PROJ AND status = "To Do" ORDER BY priority DESC'
        client.search_issues(jql)

    finally:
        client.close()


if __name__ == "__main__":
    main()
