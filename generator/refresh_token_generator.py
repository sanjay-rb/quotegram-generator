from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import os

ENV_FILE = ".env"


def update_env_file(key: str, value: str):
    """
    Updates or adds a key=value pair in the .env file.
    """
    env_path = Path(ENV_FILE)

    # If no .env exists, create one directly
    if not env_path.exists():
        with open(env_path, "w") as f:
            f.write(f"{key}={value}\n")
        return

    # Load existing lines
    with open(env_path, "r") as f:
        lines = f.readlines()

    # Search for existing key
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break

    # If key not found, append it
    if not updated:
        lines.append(f"{key}={value}\n")

    # Rewrite file
    with open(env_path, "w") as f:
        f.writelines(lines)


# Run OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secrets.json", scopes=["https://www.googleapis.com/auth/youtube.upload"]
)

creds = flow.run_local_server(port=8080)

# Extract credential values
access_token = creds.token
refresh_token = creds.refresh_token
client_id = creds.client_id
client_secret = creds.client_secret
token_uri = creds.token_uri

# Write values to .env
update_env_file("YOUTUBE_ACCESS_TOKEN", access_token)
update_env_file("YOUTUBE_REFRESH_TOKEN", refresh_token)
update_env_file("YOUTUBE_CLIENT_ID", client_id)
update_env_file("YOUTUBE_CLIENT_SECRET", client_secret)
update_env_file("YOUTUBE_TOKEN_URI", token_uri)

print("✔ Tokens successfully saved to .env")
