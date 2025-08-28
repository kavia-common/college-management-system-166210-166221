import base64
import hmac
import json
import time
from hashlib import sha256
from typing import Optional, Dict
from flask import current_app


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


# PUBLIC_INTERFACE
def create_access_token(user_id: int, role: str) -> str:
    """Create a signed access token for a user with expiry from config."""
    secret = current_app.config["SECRET_KEY"].encode()
    exp_mins = int(current_app.config.get("ACCESS_TOKEN_EXPIRES_MINUTES", 60))
    payload = {"sub": user_id, "role": role, "exp": int(time.time()) + exp_mins * 60}
    header = {"alg": "HS256", "typ": "JWT-lite"}

    header_b64 = _b64encode(json.dumps(header).encode())
    payload_b64 = _b64encode(json.dumps(payload).encode())
    to_sign = f"{header_b64}.{payload_b64}".encode()

    signature = hmac.new(secret, to_sign, sha256).digest()
    sig_b64 = _b64encode(signature)
    return f"{header_b64}.{payload_b64}.{sig_b64}"


# PUBLIC_INTERFACE
def verify_access_token(token: str) -> Optional[Dict]:
    """Verify token signature and expiry. Returns payload dict if valid else None."""
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
        to_sign = f"{header_b64}.{payload_b64}".encode()
        signature = _b64decode(sig_b64)
        expected = hmac.new(current_app.config["SECRET_KEY"].encode(), to_sign, sha256).digest()
        if not hmac.compare_digest(signature, expected):
            return None
        payload = json.loads(_b64decode(payload_b64))
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload
    except Exception:
        return None
