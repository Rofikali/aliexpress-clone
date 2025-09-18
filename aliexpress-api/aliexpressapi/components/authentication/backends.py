

# # components/authentication/backends.py
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.exceptions import AuthenticationFailed


# class CustomJWTAuthentication(JWTAuthentication):
#     """
#     Thin wrapper around SimpleJWT's JWTAuthentication.
#     Keep decoding/validation to SimpleJWT. Add only project-level checks here.
#     """

#     def get_user(self, validated_token):
#         """
#         validated_token is the token dict returned by SimpleJWT; parent resolves user.
#         We call super().get_user() then add business checks.
#         """
#         user = super().get_user(validated_token)

#         # Example: disable inactive users
#         if not user.is_active:
#             raise AuthenticationFailed("User account is inactive")

#         # Optionally: enforce email verification at *permission* level, not here.
#         # if not user.is_email_verified:
#         #     raise AuthenticationFailed("Email not verified")

#         # Add any device/session validation here later (DB lookup) using validated_token["jti"]
#         return user



# components/authentication/backends.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    """
    Thin wrapper around SimpleJWT's JWTAuthentication.
    All decoding/validation done by SimpleJWT.
    Add project-specific checks here (inactive, KYC, tenant, device checks).
    """

    def get_user(self, validated_token):
        """
        validated_token is a SimpleJWT token-like mapping.
        Parent implementation resolves the user instance.
        We add small business checks here.
        """
        user = super().get_user(validated_token)

        # Example: disallow inactive users
        if not user.is_active:
            raise AuthenticationFailed("User account is inactive")

        # NOTE: Prefer enforcing email verification in TokenObtainPair serializer
        # or in a Permission class, rather than in authentication, unless you
        # absolutely want to block every authenticated request.

        return user
