from langchain.tools import tool
import os
import requests
from dotenv import load_dotenv
from github_gchat_agent.integrations.refreshgooglechattoken import get_token



@tool
def get_issues(repo: str, state: str = "open") -> list:
    """Get issues on a repository in github by its name. Pass state of prs to filter"""

    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")
    USER = os.getenv("USER_GITHUB")
    if state:
        url = f"https://api.github.com/repos/{USER}/{repo}/issues?state={state}"
    else:
        url = f"https://api.github.com/repos/{USER}/{repo}/issues"

    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2026-03-10",
        }


        response = requests.get(url, headers=headers)
        response.raise_for_status()
        res = response.json()

        return [
            {
                "title": issue.get("title"),
                "assignees": [a.get("login") for a in issue.get("assignees", [])],
                "state": issue.get("state"),
                "url": issue.get("html_url"),
            }
            for issue in res
        ]
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        return []



@tool
def get_open_pullrequests(repo: str) -> list:
    """Get pull requests on a repository in github from its name"""

    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")
    USER = os.getenv("USER_GITHUB")
    url = f"https://api.github.com/repos/{USER}/{repo}/pulls"

    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2026-03-10",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        prs = response.json()
        return [
            {
                "number": pr.get("number"),
                "title": pr.get("title"),
                "body": pr.get("body"),
                "url": pr.get("html_url"),
                "author": pr.get("user", {}).get("login"),
                "state": pr.get("state"),
            }
            for pr in prs
        ]
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        return []



@tool 
def send_message_google_chat(message: str) -> str:
    """send message to the google chat workspace"""

    print("message from google chat: " + message)
    SPACE_ID = os.getenv("GCHAT_SPACE_ID")

    GOOGLE_CHAT_ACCESS_TOKEN=get_token()

    print(message)

    # url = f"https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages"


    # headers = {
    #     "Authorization": f"Bearer {GOOGLE_CHAT_ACCESS_TOKEN}",
    #     "Content-Type": "application/json",
    # }

    # print(GOOGLE_CHAT_ACCESS_TOKEN)

    # data = {
    #     "text": message
    # }

    # try:
    #     response = requests.post(
    #         url,
    #         headers=headers,
    #         json=data,
    #         timeout=30
    #     )

    #     response.raise_for_status()

    #     print("Message sent successfully!")
    #     print(response.json())
    #     return "Message sent successfully!"

    # except requests.exceptions.HTTPError as ex:
    #     print(f"HTTP error: {ex}")
    #     print(f"Response: {response.text}")
    #     return f"HTTP error: {ex}"

    # except requests.exceptions.RequestException as ex:
    #     print(f"Request failed: {ex}")
    #     return f"Request failed: {ex}"
    # except Exception as ex:
    #     print(f"Unexpected error: {ex}")
    #     return f"Unexpected error: {ex}"
    return []

