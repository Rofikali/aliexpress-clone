from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

from apps.accounts.models.kyc import KYCApplication


class EnforceKYCApprovalMiddleware(MiddlewareMixin):
    EXEMPT_PATHS = [
        "/api/v1/auth/login/",
        "/api/v1/auth/register/",
        "/api/v1/auth/logout/",
        "/api/v1/auth/refresh/",
        "/api/v1/profile/",
        "/api/v1/kyc/",
        "/admin/",
    ]

    PROTECTED_NAMESPACES = ["orders", "payments", "withdrawals"]

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not settings.ENFORCE_KYC:
            return None  # Skip enforcement in dev/local

        path = request.path
        if any(path.startswith(exempt) for exempt in self.EXEMPT_PATHS):
            return None

        if not request.user.is_authenticated:
            return None  # DRF handles unauthenticated requests

        resolver_match = resolve(path)
        app_name = resolver_match.app_name or resolver_match.namespace

        if app_name in self.PROTECTED_NAMESPACES:
            try:
                app = KYCApplication.objects.get(user=request.user)
                if app.status != KYCApplication.STATUS_APPROVED:
                    return JsonResponse(
                        {
                            "detail": "Your KYC must be approved to access this resource."
                        },
                        status=403,
                    )
            except KYCApplication.DoesNotExist:
                return JsonResponse(
                    {
                        "detail": "KYC submission required before accessing this resource."
                    },
                    status=403,
                )

        return None
