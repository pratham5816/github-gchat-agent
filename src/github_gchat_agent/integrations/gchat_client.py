"""
Skeleton client for handling Google Chat payload extraction and message formatting.
"""
from typing import Dict, Any

def parse_incoming_gchat_payload(payload: Dict[str, Any]) -> str:
    """Extracts user prompt text and sender info from Google Chat event payload."""
    message = payload.get("message", {})
    user_text = message.get("argumentText", "").strip() or message.get("text", "").strip()
    sender_name = message.get("sender", {}).get("displayName", "User")
    print(f"--> [GChat Client] Extracted message from '{sender_name}': '{user_text}'")
    return user_text

def format_gchat_reply(reply_text: str) -> Dict[str, Any]:
    """Formats the reply string into a standard Google Chat message payload."""
    return {
        "text": reply_text
    }
