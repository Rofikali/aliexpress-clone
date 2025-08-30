# # # from .views import PostViewSet
# # # from rest_framework.routers import DefaultRouter
# # # from django.urls import path
# # # from .views import (
# # #     LoggedInUser,
# # #     UpdateUserImage,
# # #     GetUser,
# # #     UpdateUser,
# # #     PostCreateView,
# # #     PostDetailView,
# # #     PostDeleteView,
# # #     LikeCreateView, LikeDeleteView, CommentCreateView, CommentDeleteView,
# # #     HomeView,
# # #     ProfileView,
# # #     GlobalView,
# # #     LoginView, LogoutView,
# # #     SendVerificationEmail, VerifyEmail,
# # #     RequestPasswordReset, ResetPassword,
# # #     PasswordResetLinkController,
# # #     RegisterUserView,
# # #     VerifyEmailView,

# # # )

# # # urlpatterns = [
# # #     path('user/logged-in/', LoggedInUser.as_view(), name='logged_in_user'),
# # #     path('user/update-image/', UpdateUserImage.as_view(), name='update_user_image'),
# # #     path('user/<int:id>/', GetUser.as_view(), name='get_user'),
# # #     path('user/update/', UpdateUser.as_view(), name='update_user'),
# # #     path('posts/create/', PostCreateView.as_view(), name='post_create'),
# # #     path('posts/<int:id>/', PostDetailView.as_view(), name='post_detail'),
# # #     path('posts/<int:id>/delete/', PostDeleteView.as_view(), name='post_delete'),
# # #     path('likes/create/', LikeCreateView.as_view(), name='like_create'),
# # #     path('likes/<int:id>/delete/', LikeDeleteView.as_view(), name='like_delete'),
# # #     path('comments/create/', CommentCreateView.as_view(), name='comment_create'),
# # #     path('comments/<int:id>/delete/',
# # #          CommentDeleteView.as_view(), name='comment_delete'),
# # #     path('home/', HomeView.as_view(), name='home_index'),
# # #     path('profile/<int:id>/', ProfileView.as_view(), name='profile_show'),
# # #     path('global/random-users/', GlobalView.as_view(), name='random_users'),
# # #     path('login/', LoginView.as_view(), name='login'),
# # #     path('logout/', LogoutView.as_view(), name='logout'),
# # #     path('send-verification/', SendVerificationEmail.as_view(),
# # #          name='send_verification_email'),
# # #     path('verify-email/<str:uidb64>/<str:token>/',
# # #          VerifyEmail.as_view(), name='email_verification'),
# # #     path('request-password-reset/', RequestPasswordReset.as_view(),
# # #          name='password_reset_request'),
# # #     path('reset-password/<str:uidb64>/<str:token>/',
# # #          ResetPassword.as_view(), name='password_reset_confirm'),
# # #     path('password-reset/', PasswordResetLinkController.as_view(),
# # #          name='password_reset_request'),
# # #     path('register/', RegisterUserView.as_view(), name='register_user'),
# # #     path('verify-email/<uidb64>/<token>/',
# # #          VerifyEmailView.as_view(), name='verify_email'),
# # # ]


# # # router = DefaultRouter()
# # # router.register(r'posts', PostViewSet, basename='post')
# # # urlpatterns = router.urls


# # # from .views import PostViewSet
# # from rest_framework.routers import DefaultRouter
# # from django.urls import path
# # from .views import (
# #     LoggedInUser,
# #     UpdateUserImage,
# #     GetUser,
# #     UpdateUser,
# #     PostCreateView,
# #     PostDetailView,
# #     PostDeleteView,
# #     #     LikeCreateView,
# #     #     LikeDeleteView,
# #     #     CommentCreateView,
# #     #     CommentDeleteView,
# #     HomeView,
# #     ProfileView,
# #     GlobalView,
# #     LoginView,
# #     LogoutView,
# #     SendVerificationEmail,
# #     VerifyEmail,
# #     RequestPasswordReset,
# #     ResetPassword,
# #     PasswordResetLinkController,
# #     RegisterUserView,
# #     VerifyEmailView,
# #     #     CSRFTokenView
# #     CSRFTokenViewSet,
# # )

# # # Define your URL patterns
# # urlpatterns = [
# #     path("user/logged-in-user/", LoggedInUser.as_view(), name="logged_in_user"),
# #     #     path('user/logged-in/', LoggedInUser.as_view(), name='logged_in_user'),
# #     path("user/update-image/", UpdateUserImage.as_view(), name="update_user_image"),
# #     path("user/<int:id>/", GetUser.as_view(), name="get_user"),
# #     path("user/update/", UpdateUser.as_view(), name="update_user"),
# #     path("posts/create/", PostCreateView.as_view(), name="post_create"),
# #     path("posts/<int:id>/", PostDetailView.as_view(), name="post_detail"),
# #     path("posts/<int:id>/delete/", PostDeleteView.as_view(), name="post_delete"),
# #     #     path('likes/create/', LikeCreateView.as_view(), name='like_create'),
# #     #     path('likes/<int:id>/delete/', LikeDeleteView.as_view(), name='like_delete'),
# #     #     path('comments/create/', CommentCreateView.as_view(), name='comment_create'),
# #     #     path('comments/<int:id>/delete/',
# #     #          CommentDeleteView.as_view(), name='comment_delete'),
# #     path("home/", HomeView.as_view(), name="home_index"),
# #     # path('posts/', HomeView.as_view(), name='home_index'),
# #     path("profiles/<int:id>/", ProfileView.as_view(), name="profile_show"),
# #     path("get-random-users/", GlobalView.as_view(), name="random_users"),
# #     path("login/", LoginView.as_view(), name="login"),
# #     path("logout/", LogoutView.as_view(), name="logout"),
# #     path(
# #         "send-verification/",
# #         SendVerificationEmail.as_view(),
# #         name="send_verification_email",
# #     ),
# #     path(
# #         "verify-email/<str:uidb64>/<str:token>/",
# #         VerifyEmail.as_view(),
# #         name="email_verification",
# #     ),
# #     path(
# #         "request-password-reset/",
# #         RequestPasswordReset.as_view(),
# #         name="password_reset_request",
# #     ),
# #     path(
# #         "reset-password/<str:uidb64>/<str:token>/",
# #         ResetPassword.as_view(),
# #         name="password_reset_confirm",
# #     ),
# #     path(
# #         "password-reset/",
# #         PasswordResetLinkController.as_view(),
# #         name="password_reset_request",
# #     ),
# #     path("register", RegisterUserView.as_view(), name="register_user"),
# #     path(
# #         "verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify_email"
# #     ),
# #     #     path('sanctum/csrf-cookie/', CSRFTokenView.as_view(), name='csrf_cookie'),\
# #     path(
# #         "sanctum/csrf-cookie/",
# #         CSRFTokenViewSet.as_view({"get": "list"}),
# #         name="csrf_cookie",
# #     ),
# # ]

# # Create and register router for the PostViewSet
# # router = DefaultRouter()
# # router.register(r'posts', PostViewSet, basename='post')

# # # Combine the manual URLs and router-generated URLs
# # urlpatterns += router.urls


# from inspect import getmembers, isclass

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from rest_framework.viewsets import ViewSet

# from . import views

# router = DefaultRouter()

# # Automatically find all ViewSets in views.py and register them
# for name, cls in getmembers(views, isclass):
#     if issubclass(cls, ViewSet) and cls.__module__ == views.__name__:
#         router.register(
#             rf"{name.lower().replace('viewset', '')}", cls, basename=name.lower()
#         )

# # router.register(r"productlist", views.ProductListViewSet, basename="productlist")


# urlpatterns = [
#     # Register the routes under '/api/mod5/'
#     path("", include(router.urls)),
#     # 🚀 Nested routes with dynamic user ID
#     # path(
#     #     "profile/<int:user_id>/posts/",
#     #     views.ProfilePostViewSet.as_view({"get": "list"}),
#     #     name="profile-posts",
#     # ),
#     # Manually add the custom path for DynamicCategoryURLFilterViewSet
# ]

from inspect import getmembers, isclass

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet

from . import views

router = DefaultRouter()

# Automatically find all ViewSets in views.py and register them
for name, cls in getmembers(views, isclass):
    if issubclass(cls, ViewSet) and cls.__module__ == views.__name__:
        router.register(
            rf"{name.lower().replace('viewset', '')}", cls, basename=name.lower()
        )

urlpatterns = [
    path("", include(router.urls)),  # Register the routes under '/api/products/'
]
