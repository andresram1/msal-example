# ======================================================================================================================
# JOSE Definitions
# https://python-jose.readthedocs.io/en/latest/
# JSON Web Signatures (JWS) are used to digitally sign a JSON encoded object and represent it as a compact
# URL-safe string.
# JSON Web Keys (JWK) are a JSON data structure representing a cryptographic key
# JSON Web Tokens (JWT) are a JWS with a set of reserved claims to be used in a standardized manner.
# ======================================================================================================================

from flask import request
from functools import wraps
from jose import jwt


# Error handler
class AuthError(Exception):
    """
    Class that handles Authorization Exceptions if any
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Formats error response and append status code
def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must start with Bearer"}, 401)

    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """
    Determines if the Access Token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()

        # TODO Check if the JWT is valid
        unverified_header = jwt.get_unverified_header(token)
        if unverified_header['typ'] == 'JWT':
            return f(*args, **kwargs)

        raise AuthError({"code": "invalid_header", "description": "Unable to find appropriate key"}, 401)

    return decorated
