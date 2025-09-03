# """
# components/authentication/jwt_utils.py

# Wrapper utilities around djangorestframework-simplejwt.
# Provides:
#  - create_token_pair_for_user(user, session_jti=None)
#  - decode_access(token), decode_refresh(token)
#  - refresh_access_token(refresh_token)  # returns new access (+ optionally refresh depending on config)
#  - blacklist_refresh_token(refresh_token)
#  - token_expiry_info(token)  # returns (exp_timestamp, is_expired_bool)
#  - add_custom_claims(token_obj, claims_dict)  # helper to attach claims to RefreshToken/AccessToken
# """

# import logging
# from typing import Dict, Optional, Tuple, Any

# from django.conf import settings
# from django.utils import timezone

# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, Token
# from rest_framework_simplejwt.exceptions import TokenError

# logger = logging.getLogger(__name__)

# # Config helpers
# SIMPLE_JWT_CONF = getattr(settings, "SIMPLE_JWT", {})
# ROTATE_REFRESH = SIMPLE_JWT_CONF.get("ROTATE_REFRESH_TOKENS", True)
# BLACKLIST_AFTER_ROTATION = SIMPLE_JWT_CONF.get("BLACKLIST_AFTER_ROTATION", True)


# def _now_ts() -> int:
#     return int(timezone.now().timestamp())


# def create_token_pair_for_user(
#     user, session_jti: Optional[str] = None
# ) -> Dict[str, str]:
#     """
#     Create refresh + access tokens for user.
#     Optionally set 'jti' claim to session_jti so DB session rows can be bound to tokens.
#     Returns {"access": <str>, "refresh": <str>}
#     """
#     refresh = RefreshToken.for_user(user)

#     # attach session id if provided (helps keeping RefreshSession.jti in sync)
#     if session_jti:
#         refresh["jti"] = str(session_jti)

#     # Example custom claims (project-specific):
#     # safe to add small, non-sensitive flags like role, tenant, kyc
#     if hasattr(user, "role"):
#         refresh["role"] = getattr(user, "role", "user")
#     if hasattr(user, "is_kyc_verified"):
#         refresh["is_kyc_verified"] = bool(getattr(user, "is_kyc_verified", False))

#     # create access token from refresh token (propagates those claims)
#     access = refresh.access_token
#     # attach any access-only claims if needed
#     # access["some_claim"] = "value"

#     return {"access": str(access), "refresh": str(refresh)}


# def decode_access(token: str) -> Dict[str, Any]:
#     """
#     Decode an access token and return the claims dict.
#     Raises TokenError on invalid/expired tokens.
#     """
#     try:
#         at = AccessToken(token)
#         return dict(at)  # convert token-like object to dict of claims
#     except TokenError as exc:
#         logger.debug("Access token decode error: %s", exc)
#         raise


# def decode_refresh(token: str) -> Dict[str, Any]:
#     """
#     Decode a refresh token and return claims dict.
#     Raises TokenError on invalid/expired tokens.
#     """
#     try:
#         rt = RefreshToken(token)
#         return dict(rt)
#     except TokenError as exc:
#         logger.debug("Refresh token decode error: %s", exc)
#         raise


# def refresh_access_token(refresh_token: str) -> Dict[str, str]:
#     """
#     Given a refresh token, produce a new access token.
#     If ROTATE_REFRESH is True (SimpleJWT config), you should handle refresh rotation at a higher level
#     (SimpleJWT's RefreshToken().rotate() / blacklist behavior is used by its views).
#     This helper returns {'access': <str>, 'refresh': <str or original depending on rotation>}
#     """
#     try:
#         rt = RefreshToken(refresh_token)
#     except TokenError as exc:
#         logger.warning("refresh_access_token: invalid refresh token: %s", exc)
#         raise

#     # access token from refresh
#     access_token = rt.access_token

#     # If config asks to rotate, the calling code (view) should create a new RefreshToken
#     # SimpleJWT's `TokenRefreshView` handles rotation & blacklisting when configured.
#     return {"access": str(access_token), "refresh": refresh_token}


# def blacklist_refresh_token(refresh_token: str) -> bool:
#     """
#     Blacklist the given refresh token using SimpleJWT's blacklist support.
#     Returns True if blacklisting succeeded (or if token already blacklisted).
#     Returns False on failure (invalid token or blacklist app not installed).
#     """
#     try:
#         rt = RefreshToken(refresh_token)
#         rt.blacklist()
#         logger.info(
#             "Blacklisted refresh token for subject=%s jti=%s",
#             rt.get("sub"),
#             rt.get("jti"),
#         )
#         return True
#     except Exception as exc:
#         # TokenError, AttributeError (if blacklist app not installed), etc.
#         logger.warning("Failed to blacklist refresh token: %s", exc)
#         return False


# def token_expiry_info(token: str) -> Tuple[Optional[int], bool]:
#     """
#     Returns (expiry_ts, is_expired_bool).
#     expiry_ts is unix timestamp or None if invalid.
#     """
#     try:
#         # Try access then refresh, whichever parses
#         obj = None
#         try:
#             obj = AccessToken(token)
#         except TokenError:
#             obj = RefreshToken(token)
#         exp = int(obj["exp"])
#         now_ts = _now_ts()
#         return exp, exp <= now_ts
#     except Exception:
#         return None, True


# def add_custom_claims(token_obj: Token, claims: Dict[str, Any]) -> Token:
#     """
#     Attach claims onto a Token-like object (AccessToken or RefreshToken).
#     Returns the token_obj for chaining.
#     """
#     for k, v in claims.items():
#         token_obj[k] = v
#     return token_obj


# components/authentication/jwt_utils.py
"""
Wrapper utilities around djangorestframework-simplejwt.

Provides:
 - create_token_pair_for_user(user, session_jti=None)
 - decode_access(token), decode_refresh(token)
 - refresh_access_token(refresh_token)           # returns new access (+ rotated refresh if enabled)
 - blacklist_refresh_token(refresh_token)
 - token_expiry_info(token)                      # returns (exp_timestamp, is_expired_bool)
 - add_custom_claims(token_obj, claims_dict)    # helper to attach claims to RefreshToken/AccessToken
"""

import logging
from typing import Dict, Optional, Tuple, Any
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, Token
from rest_framework_simplejwt.exceptions import TokenError

logger = logging.getLogger(__name__)

# Config helpers
SIMPLE_JWT_CONF = getattr(settings, "SIMPLE_JWT", {})
ROTATE_REFRESH = SIMPLE_JWT_CONF.get("ROTATE_REFRESH_TOKENS", True)
BLACKLIST_AFTER_ROTATION = SIMPLE_JWT_CONF.get("BLACKLIST_AFTER_ROTATION", True)
JWT_ACCESS_COOKIE = getattr(settings, "JWT_ACCESS_COOKIE", "")


def _now_ts() -> int:
    return int(timezone.now().timestamp())


def _attach_standard_claims(
    refresh: RefreshToken, user, session_jti: Optional[str]
) -> None:
    """
    Attach standard/custom claims consistently.
    We standardize on 'sub' for user PK.
    """
    refresh["sub"] = str(user.pk)  # single source of truth for subject
    if session_jti:
        refresh["jti"] = str(session_jti)

    # Example custom claims (small, non-sensitive)
    if hasattr(user, "role"):
        refresh["role"] = getattr(user, "role", "user")
    if hasattr(user, "is_kyc_verified"):
        refresh["is_kyc_verified"] = bool(getattr(user, "is_kyc_verified", False))


# utils/jwt_utils.py (or wherever you keep token helpers)
def create_token_pair_for_user(user):
    """
    Create a refresh + access token pair for the given user,
    with proper expiry handling and Django 5.x safe timezone usage.
    """
    refresh = RefreshToken.for_user(user)
    _attach_standard_claims(refresh, user, session_jti=None)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Access token expiry from token payload (avoid manual timedelta math)
    exp_ts = int(refresh.access_token["exp"])
    access_expires_at = datetime.fromtimestamp(exp_ts, tz=timezone.utc)

    return {
        "access": access_token,
        "refresh": refresh_token,
        "access_expires_at": access_expires_at.isoformat(),
        "sub": str(user.id),
    }


# def create_token_pair_for_user(user):
#     """
#     Create a refresh + access token pair for the given user,
#     with proper expiry handling and Django 5.x safe timezone usage.
#     """
#     refresh = RefreshToken.for_user(user)

#     access_token = str(refresh.access_token)
#     refresh_token = str(refresh)

#     # Access token expiry time (use timezone.utc, not django.utils.timezone.utc)
#     access_expires_at = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(
#         seconds=refresh.access_token.lifetime.total_seconds()
#     )

#     return {
#         "access": access_token,
#         "refresh": refresh_token,
#         "access_expires_at": access_expires_at.isoformat(),
#         "sub": str(user.id),  # ✅ Standard JWT 'sub' claim (subject = user.id)
#     }


def decode_access(token: str) -> Dict[str, Any]:
    """Decode an access token and return the claims dict. Raises TokenError on invalid/expired tokens."""
    try:
        at = AccessToken(token)
        return dict(at)
    except TokenError as exc:
        logger.debug("Access token decode error: %s", exc)
        raise


def decode_refresh(token: str) -> Dict[str, Any]:
    """Decode a refresh token and return the claims dict. Raises TokenError on invalid/expired tokens."""
    try:
        rt = RefreshToken(token)
        return dict(rt)
    except TokenError as exc:
        logger.debug("Refresh token decode error: %s", exc)
        raise


def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
    """
    Given a refresh token, produce a new access token and optionally rotate refresh.
    Returns:
      {'access': <str>, 'access_expires_at': <datetime>, 'refresh': <str>}
    """
    try:
        rt = RefreshToken(refresh_token)
    except TokenError as exc:
        logger.warning("refresh_access_token: invalid refresh token: %s", exc)
        raise

    # new access from provided refresh
    access = rt.access_token
    exp_ts = int(access["exp"])
    access_expires_at = timezone.datetime.fromtimestamp(exp_ts, tz=timezone.utc)

    # Rotate if configured: issue a NEW refresh for the same user + copy light claims
    new_refresh_str = refresh_token
    if ROTATE_REFRESH:
        try:
            sub = rt.get("sub") or rt.get("user_id") or rt.get("user")
            if not sub:
                raise TokenError("Refresh token missing 'sub'")
            User = get_user_model()
            user = User.objects.get(pk=sub)

            new_refresh = RefreshToken.for_user(user)
            # propagate standard/custom claims (incl. role/kyc). Do NOT reuse old jti.
            _attach_standard_claims(new_refresh, user, session_jti=None)
            new_refresh_str = str(new_refresh)

            if BLACKLIST_AFTER_ROTATION:
                try:
                    rt.blacklist()
                except Exception as be:
                    logger.info(
                        "Blacklist after rotation failed or not enabled: %s", be
                    )
        except Exception as exc:
            logger.exception(
                "Rotation failure, falling back to original refresh: %s", exc
            )
            new_refresh_str = refresh_token

    return {
        "access": str(access),
        "access_expires_at": access_expires_at,
        "refresh": new_refresh_str,
    }


def blacklist_refresh_token(refresh_token: str) -> bool:
    """
    Blacklist the given refresh token using SimpleJWT's blacklist support.
    Returns True if blacklisting succeeded (or if token already blacklisted).
    Returns False on failure (invalid token or blacklist app not installed).
    """
    try:
        rt = RefreshToken(refresh_token)
        rt.blacklist()
        logger.info(
            "Blacklisted refresh token for sub=%s jti=%s", rt.get("sub"), rt.get("jti")
        )
        return True
    except Exception as exc:
        logger.warning("Failed to blacklist refresh token: %s", exc)
        return False


def token_expiry_info(token: str) -> Tuple[Optional[int], bool]:
    """Returns (expiry_ts, is_expired_bool). expiry_ts is unix timestamp or None if invalid."""
    try:
        obj: Token
        try:
            obj = AccessToken(token)
        except TokenError:
            obj = RefreshToken(token)
        exp = int(obj["exp"])
        now_ts = _now_ts()
        return exp, exp <= now_ts
    except Exception:
        return None, True


def add_custom_claims(token_obj: Token, claims: Dict[str, Any]) -> Token:
    """Attach claims onto a Token-like object (AccessToken or RefreshToken)."""
    for k, v in claims.items():
        token_obj[k] = v
    return token_obj
