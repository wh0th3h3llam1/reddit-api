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
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_nested import routers

from post.views import CommentViewSet, PostViewSet
from subreddit.views import SubredditLinkViewSet, SubredditViewSet
from users.views import UserViewSet


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

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/signup/", include("dj_rest_auth.registration.urls")),
    path("api/", include(user_router.urls)),
    path("api/", include(router.urls)),
    path("api/", include(post_router.urls)),
    path("api/", include(comment_router.urls)),
    path("api/", include(subreddit_link_router.urls)),
]

urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]
