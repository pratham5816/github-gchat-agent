import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from google_auth_oauthlib.flow import Flow

SCOPES = [
    "https://www.googleapis.com/auth/chat.messages.create"
]

REDIRECT_URI = "http://localhost:8080"

flow = Flow.from_client_secrets_file(
    "credentials.json",
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

with open("token.json", "w") as file:
    file.write(credentials.to_json())

print("\nAuthorization successful!")
print("Access token:", credentials.token)
print("Refresh token:", credentials.refresh_token)
print("Tokens saved to token.json")