# import jwt
# import datetime
# from django.conf import settings
# from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


# def generate_jwt(payload, expires_in=3600):
#     """
#     Generate JWT token.
#     :param payload: dict
#     :param expires_in: seconds (default: 1 hour)
#     """
#     payload_copy = payload.copy()
#     payload_copy["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
#         seconds=expires_in
#     )
#     token = jwt.encode(payload_copy, settings.SECRET_KEY, algorithm="HS256")
#     return token


# def decode_jwt(token):
#     """
#     Decode JWT token.
#     """
#     try:
#         decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         return decoded
#     except ExpiredSignatureError:
#         return {"error": "Token expired"}
#     except InvalidTokenError:
#         return {"error": "Invalid token"}


from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
