"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_nested import routers

from post.views import CommentViewSet, PostViewSet
from subreddit.views import SubredditLinkViewSet, SubredditViewSet
from users.views import UserDetailView, UserViewSet


router = routers.SimpleRouter()

router.register(prefix=r"r", viewset=SubredditViewSet, basename="subreddits")

post_router = routers.NestedSimpleRouter(
    parent_router=router, parent_prefix=r"r", lookup="subreddit"
)
post_router.register(prefix=r"posts", viewset=PostViewSet, basename="posts")

comment_router = routers.NestedSimpleRouter(
    parent_router=post_router, parent_prefix=r"posts", lookup="posts"
)
comment_router.register(
    prefix=r"comments", viewset=CommentViewSet, basename="comments"
)

subreddit_link_router = routers.NestedSimpleRouter(
    parent_router=router, parent_prefix="r", lookup="subreddit"
)
subreddit_link_router.register(
    prefix="links", viewset=SubredditLinkViewSet, basename="subreddit-links"
)

user_router = routers.SimpleRouter()

user_router.register(prefix="u", viewset=UserViewSet, basename="users")


router_urls = [
    path("", include(user_router.urls)),
    path("", include(router.urls)),
    path("", include(post_router.urls)),
    path("", include(comment_router.urls)),
    path("", include(subreddit_link_router.urls)),
]

dj_rest_auth_urls = [
    # URLs that do not require a session or valid token
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path("signup/", include("dj_rest_auth.registration.urls")),
    path("login/", LoginView.as_view(), name="rest_login"),
    # URLs that require a user to be logged in with a valid session / token.
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path(
        "password/change/",
        PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path("user/", UserDetailView.as_view(), name="rest_user"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(dj_rest_auth_urls)),
    path("api/", include(router_urls)),
]

urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
