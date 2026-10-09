"""
Skeleton client for interacting with the GitHub API.
"""

def fetch_github_pull_requests(repo_name: str) -> str:
    """Simulates fetching open pull requests from GitHub."""
    return f"[GitHub Client] Fetched 2 open PRs for '{repo_name}': [#101 'Fix auth bug', #102 'Add webhook handler']"

def fetch_github_issues(repo_name: str) -> str:
    """Simulates fetching issues from GitHub."""
    return f"[GitHub Client] Fetched 1 open issue for '{repo_name}': [#55 'Document API endpoints']"
