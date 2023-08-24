from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from common.constants import PostType
from common.mixins import SerializerActionClassMixin
from post.models import Post
from post.serializers.post_serializers import PostListSerializer
from users.filters import UserHomeFeedFilterSet
from users.models import User
from users.serializers import UserSerializer

# Create your views here.


@extend_schema(tags=["Users"])
class UserViewSet(
    SerializerActionClassMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {"feed": PostListSerializer}
    lookup_field = "username"

    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = UserHomeFeedFilterSet

    @action(
        methods=["GET"], detail=False, permission_classes=(IsAuthenticated,)
    )
    def feed(self, request, *args, **kwargs):
        feed_type = request.query_params.get("feed_type", "subscribed")
        post_type = request.query_params.get("post_type", None)
        ordering = request.query_params.get("ordering", "-created")

        if feed_type not in ["subscribed", "all"]:
            return Response(
                data={"message": "`feed_type` must be a valid choice."},
                status=HTTP_400_BAD_REQUEST,
            )

        if post_type not in PostType.values() and post_type is not None:
            return Response(
                data={"message": "`post_type` must be a valid choice."},
                status=HTTP_400_BAD_REQUEST,
            )

        # if (
        #     ordering
        #     not in [
        #         "new",
        #         "best",
        #         "hot",
        #         "rising",
        #         "controversial",
        #         "random",
        #     ]
        #     and ordering is not None
        # ):
        #     return Response(
        #         data={"message": "`ordering` must be a valid choice."},
        #         status=HTTP_400_BAD_REQUEST,
        #     )

        posts = Post.objects.all()
        if feed_type == "subscribed":
            subreddits = set(
                request.user.joined_subreddits.values_list(
                    "subreddit__id", flat=True
                )
            )
            posts = posts.filter(subreddit__in=subreddits)

        if post_type is not None:
            posts = posts.filter(post_type=post_type)

        # if ordering:
        #     posts = posts.order_by("-created")

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
