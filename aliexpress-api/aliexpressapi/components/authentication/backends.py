# """
# components/authentication/backends.py

# Custom DRF authentication backend that:
#  - supports Authorization: Bearer <token> header
#  - supports cookie-mode if JWT_ACCESS_COOKIE is configured
#  - delegates decoding to jwt_utils (SimpleJWT wrapper)
#  - validates user exists and is active
#  - optional device/session validation against RefreshSession (if you have such model)
#  - logs suspicious events
# """

# import logging
# from typing import Optional, Tuple

# from django.conf import settings
# from django.contrib.auth import get_user_model
# from rest_framework.authentication import BaseAuthentication, get_authorization_header
# from rest_framework.exceptions import AuthenticationFailed

# from components.authentication import jwt_utils

# logger = logging.getLogger(__name__)
# User = get_user_model()

# # Try to import your session model (optional). If absent, device checks are skipped.
# try:
#     # adapt this import path if your model lives elsewhere
#     from apps.accounts.models import RefreshSession  # type: ignore

#     HAS_SESSION_MODEL = True
# except Exception:
#     RefreshSession = None
#     HAS_SESSION_MODEL = False


# def _extract_bearer_token(request) -> Optional[str]:
#     """
#     Return bearer token string from Authorization header or None.
#     """
#     auth = get_authorization_header(request).split()
#     if not auth:
#         return None
#     if auth[0].lower() != b"bearer":
#         return None
#     if len(auth) == 1:
#         raise AuthenticationFailed("Invalid Authorization header.")
#     try:
#         return auth[1].decode("utf-8")
#     except Exception:
#         return None


# class CustomJWTAuthentication(BaseAuthentication):
#     """
#     DRF authentication class. Use this in REST_FRAMEWORK DEFAULT_AUTHENTICATION_CLASSES.

#     Behavior:
#       - Look for Authorization: Bearer <access_token>
#       - If not present, check cookies for JWT_ACCESS_COOKIE (if configured)
#       - Decode access token via jwt_utils.decode_access
#       - Ensure user exists and is active
#       - Optionally validate device/session if RefreshSession model exists (checks jti claim)
#     """

#     def authenticate(self, request) -> Optional[Tuple[object, None]]:
#         # header first, then cookie fallback
#         token = _extract_bearer_token(request) or request.COOKIES.get(
#             getattr(settings, "JWT_ACCESS_COOKIE", ""), None
#         )
#         if not token:
#             return None

#         try:
#             payload = jwt_utils.decode_access(token)
#         except Exception as exc:
#             logger.debug("Authentication failed: invalid access token (%s)", exc)
#             raise AuthenticationFailed("Invalid or expired access token")

#         user_id = payload.get("sub") or payload.get("user_id") or payload.get("user")
#         if not user_id:
#             logger.debug("Token missing subject claim: %s", payload)
#             raise AuthenticationFailed("Token missing subject")

#         try:
#             user = User.objects.get(id=user_id, is_active=True)
#         except User.DoesNotExist:
#             logger.warning("Authentication failed: user not found for id=%s", user_id)
#             raise AuthenticationFailed("User not found")

#         # Optional: validate session/device if jti present and you have a session model
#         jti = payload.get("jti")
#         if jti and HAS_SESSION_MODEL:
#             try:
#                 session = RefreshSession.objects.filter(
#                     user_id=user_id, jti=jti, revoked_at__isnull=True
#                 ).first()
#                 if not session or not session.is_active:
#                     logger.info(
#                         "Authentication failed: token jti not active or session revoked (user=%s jti=%s)",
#                         user_id,
#                         jti,
#                     )
#                     raise AuthenticationFailed("Token session revoked")
#             except Exception as exc:
#                 logger.exception("Error while validating session model: %s", exc)
#                 # fail closed for safety
#                 raise AuthenticationFailed("Session validation error")

#         # Log successful authentication (low volume)
#         logger.debug("Authenticated user_id=%s via JWT", user_id)
#         return (user, None)


"""
Custom DRF authentication backend that:
 - supports Authorization: Bearer <token> header
 - supports cookie-mode if JWT_ACCESS_COOKIE is configured
 - delegates decoding to jwt_utils (SimpleJWT wrapper)
 - validates user exists and is active
 - optional device/session validation against RefreshSession (if you have such model)
 - logs suspicious events
"""

import logging
from typing import Optional, Tuple

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from components.authentication import jwt_utils

logger = logging.getLogger(__name__)
User = get_user_model()

# Try to import your session model (optional). If absent, device checks are skipped.
try:
    from apps.accounts.models import RefreshSession  # type: ignore

    HAS_SESSION_MODEL = True
except Exception:
    RefreshSession = None  # type: ignore
    HAS_SESSION_MODEL = False


def _extract_bearer_token(request) -> Optional[str]:
    """Return bearer token string from Authorization header or None."""
    auth = get_authorization_header(request).split()
    if not auth:
        return None
    if auth[0].lower() != b"bearer":
        return None
    if len(auth) == 1:
        raise AuthenticationFailed("Invalid Authorization header.")
    try:
        return auth[1].decode("utf-8")
    except Exception:
        return None


class CustomJWTAuthentication(BaseAuthentication):
    """
    DRF authentication class. Use this in REST_FRAMEWORK DEFAULT_AUTHENTICATION_CLASSES.

    Behavior:
      - Look for Authorization: Bearer <access_token>
      - If not present, check cookies for JWT_ACCESS_COOKIE (if configured)
      - Decode access token via jwt_utils.decode_access
      - Ensure user exists and is active
      - Optionally validate device/session if RefreshSession model exists (checks jti claim)
    """

    def authenticate(self, request) -> Optional[Tuple[object, None]]:
        token = _extract_bearer_token(request) or request.COOKIES.get(
            getattr(settings, "JWT_ACCESS_COOKIE", ""), None
        )
        if not token:
            return None

        try:
            payload = jwt_utils.decode_access(token)
        except Exception as exc:
            logger.debug("Authentication failed: invalid access token (%s)", exc)
            raise AuthenticationFailed("Invalid or expired access token")

        # Standardized on 'sub' per jwt_utils
        user_id = payload.get("sub")
        if not user_id:
            logger.debug("Token missing 'sub' claim: %s", payload)
            raise AuthenticationFailed("Token missing subject")

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            logger.warning("Authentication failed: user not found for id=%s", user_id)
            raise AuthenticationFailed("User not found")

        # Optional device/session validation
        jti = payload.get("jti")
        if jti and HAS_SESSION_MODEL:
            try:
                session = RefreshSession.objects.filter(
                    user_id=user_id, jti=jti, revoked_at__isnull=True
                ).first()
                if not session or not getattr(session, "is_active", True):
                    logger.info(
                        "Authentication failed: token session revoked (user=%s jti=%s)",
                        user_id,
                        jti,
                    )
                    raise AuthenticationFailed("Token session revoked")
            except Exception as exc:
                logger.exception("Error while validating session model: %s", exc)
                # fail closed for safety
                raise AuthenticationFailed("Session validation error")

        logger.debug("Authenticated user_id=%s via JWT", user_id)
        return (user, None)
