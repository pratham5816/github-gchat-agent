import os
from dotenv import load_dotenv ,find_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from datetime import datetime
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/chat.messages.create"
]



def get_google_chat_credentials_prod():
    creds = Credentials(
        token=os.getenv("GOOGLE_CHAT_ACCESS_TOKEN"),
        refresh_token=os.getenv("GOOGLE_CHAT_REFRESH_TOKEN"),
        token_uri=os.getenv("GOOGLE_TOKEN_URI"),
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scopes=SCOPES,
    )


    if not creds.valid:
        try:

            creds.refresh(Request())

            # Cache the refreshed access token in memory
            os.environ["GOOGLE_CHAT_ACCESS_TOKEN"] = creds.token

        except RefreshError as exc:
            raise RuntimeError(
                f"Google Chat token refresh failed: {exc}"
            ) from exc

    return creds


def get_google_chat_credentials():
    load_dotenv(find_dotenv(), override=True)

    access_token = os.getenv("GOOGLE_CHAT_ACCESS_TOKEN")
    refresh_token = os.getenv("GOOGLE_CHAT_REFRESH_TOKEN")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    token_uri = os.getenv(
        "GOOGLE_TOKEN_URI",
        "https://oauth2.googleapis.com/token"
    )
    expiry_str = os.getenv("GOOGLE_CHAT_TOKEN_EXPIRY")
    if expiry_str:
        clean_str = expiry_str.replace("Z", "+00:00")
        expiry = datetime.fromisoformat(clean_str).replace(tzinfo=None)
    else:
        expiry = None

    if not all([access_token, refresh_token, client_id, client_secret]):
        print("Required Google OAuth credentials are missing from .env")
        return None

    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=token_uri,
        client_id=client_id,
        client_secret=client_secret,
        expiry=expiry,
        scopes=SCOPES,
    )

    if creds.valid:
        return creds

    try:
        print("Token is expired or invalid. Refreshing...")
        creds.refresh(Request())

        # Update the environment variables with refreshed credentials
        os.environ["GOOGLE_CHAT_ACCESS_TOKEN"] = creds.token
        os.environ["GOOGLE_CHAT_TOKEN_EXPIRY"] = creds.expiry.isoformat()
        # Persist updated values in .env
        update_env_file({
            "GOOGLE_CHAT_ACCESS_TOKEN": creds.token,
            "GOOGLE_CHAT_TOKEN_EXPIRY": creds.expiry.isoformat(),
        })

        return creds

    except RefreshError as exc:
        print(f"Token refresh failed: {exc}")
        return None


def update_env_file(values):
    env_path = ENV_PATH

    with open(env_path, "r") as file:
        lines = file.readlines()

    for key, value in values.items():
        updated = False

        for index, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[index] = f"{key}={value}\n"
                updated = True
                break

        if not updated:
            lines.append(f"{key}={value}\n")

    with open(env_path, "w") as file:
        file.writelines(lines)


def get_token():
    credentials = get_google_chat_credentials()
    return credentials.token if credentials else None