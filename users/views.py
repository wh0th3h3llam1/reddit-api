from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from djoser.views import UserViewSet as DjoserUserViewSet
from post.models import Post
from subreddit.models import Subreddit

from users.models import User

# Create your views here.


class UserViewSet(DjoserUserViewSet):
    def get_queryset(self):
        return super().get_queryset()

    @action(methods=["GET"], detail=False)
    def feed(self, request, *args, **kwargs):
        user: User = self.request.user

        subreddits = user.joined_subreddits.values("subreddit__name")

        Post.objects.filter(subreddit__in=subreddits).order_by("-created")

        Subreddit.objects.filter(name__in=subreddits)

        data = {}
        return Response(data, status=HTTP_200_OK)
