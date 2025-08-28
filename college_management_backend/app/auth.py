from functools import wraps
from flask import request, abort
from .token_utils import verify_access_token


def get_token_from_header() -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.lower().startswith("bearer "):
        return ""
    return auth.split(" ", 1)[1].strip()


# PUBLIC_INTERFACE
def login_required(fn):
    """Decorator that requires a valid access token in Authorization header."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_token_from_header()
        payload = verify_access_token(token)
        if not payload:
            abort(401, description="Invalid or expired token")
        request.user = payload  # attach payload to request
        return fn(*args, **kwargs)
    return wrapper


# PUBLIC_INTERFACE
def roles_required(*roles):
    """Decorator to restrict access to certain roles."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = get_token_from_header()
            payload = verify_access_token(token)
            if not payload:
                abort(401, description="Invalid or expired token")
            role = payload.get("role")
            if role not in roles:
                abort(403, description="Forbidden: insufficient role")
            request.user = payload
            return fn(*args, **kwargs)
        return wrapper
    return decorator
