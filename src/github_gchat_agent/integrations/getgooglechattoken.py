import os
from pathlib import Path
from dotenv import load_dotenv

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from google_auth_oauthlib.flow import Flow
from github_gchat_agent.integrations.refreshgooglechattoken import update_env_file

CURRENT_DIR = Path(__file__).resolve().parent
CREDENTIALS_PATH = CURRENT_DIR / "credentials.json"
TOKEN_PATH = CURRENT_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/chat.messages.create"
]

REDIRECT_URI = "http://localhost:8080"

if not CREDENTIALS_PATH.exists():
    raise FileNotFoundError(f"credentials.json not found at {CREDENTIALS_PATH}")

flow = Flow.from_client_secrets_file(
    str(CREDENTIALS_PATH),
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

auth_url, state = flow.authorization_url(
    access_type="offline",
    prompt="consent"
)

print("\nOpen this URL in your browser:\n")
print(auth_url)

authorization_response = input(
    "\nPaste the FULL redirected URL here: "
)

flow.fetch_token(
    authorization_response=authorization_response
)

credentials = flow.credentials

with open(TOKEN_PATH, "w") as file:
    file.write(credentials.to_json())

# Auto update .env with new access token and refresh token
env_updates = {
    "GOOGLE_CHAT_ACCESS_TOKEN": credentials.token,
}
if credentials.refresh_token:
    env_updates["GOOGLE_CHAT_REFRESH_TOKEN"] = credentials.refresh_token
if credentials.expiry:
    env_updates["GOOGLE_CHAT_TOKEN_EXPIRY"] = credentials.expiry.isoformat()

update_env_file(env_updates)

print("\nAuthorization successful!")
print("Access token:", credentials.token)
print("Refresh token:", credentials.refresh_token)
print(f"Tokens saved to {TOKEN_PATH} and .env updated successfully!")