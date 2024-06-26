from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from common.mixins import (
    SerializerActionClassMixin,
    PermissionActionClassMixin,
)
from common.permissions import (
    IsCommentLocked,
    IsPostLocked,
    IsSubredditMember,
    IsUserBanned,
    IsUserTheOwner,
)
from post.models import Comment, Post
from post.serializers import (
    CommentSerializer,
    CommentCreateUpdateSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
)

# Create your views here.


@extend_schema(
    tags=["Posts"],
    parameters=[
        OpenApiParameter(
            name="subreddit_name",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True,
        ),
    ],
)
class PostViewSet(
    # MultipleLookupFieldMixin,
    PermissionActionClassMixin,
    SerializerActionClassMixin,
    ModelViewSet,
):
    """Post ViewSet"""

    serializer_class = PostCreateUpdateSerializer
    serializer_action_classes = {
        "list": PostDetailSerializer,
        "retrieve": PostDetailSerializer,
    }
    lookup_field = "slug"
    # lookup_fields = ("slug", "id", "pk")
    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_action_classes = {
        "create": (IsUserBanned, IsSubredditMember),
        "update": (IsUserBanned, IsUserTheOwner, IsPostLocked),
        "partial_update": (IsUserBanned, IsUserTheOwner, IsPostLocked),
        "destroy": (IsUserBanned, IsUserTheOwner),
    }

    def get_queryset(self):
        queryset = Post.objects.all()

        if self.action == "list":
            queryset = queryset.filter(
                subreddit__name=self.kwargs["subreddit_name"]
            )
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("comments")

        return queryset

    def get_serializer(self, *args, **kwargs):
        exclude = []
        if self.action == "list":
            exclude += ("subreddit", "comments")
        if self.action == "retrieve":
            exclude += ("subreddit",)
        kwargs["exclude"] = exclude
        return super().get_serializer(*args, **kwargs)

    # @action(methods=["GET"], detail=True)
    # def comments(self, request, *args, **kwargs) -> Response:
    #     post: Post = self.get_object()
    #     serializer = CommentSerializer(
    #         post.comments.filter(parent__isnull=True),
    #         many=True,
    #     )

    #     return Response(data=serializer.data, status=HTTP_200_OK)


@extend_schema(
    tags=["Comments"],
    parameters=[
        OpenApiParameter(
            name="subreddit_name",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True,
        ),
        OpenApiParameter(
            name="posts_slug",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True,
        ),
    ],
)
class CommentViewSet(
    PermissionActionClassMixin, SerializerActionClassMixin, ModelViewSet
):
    """Comment ViewSet"""

    serializer_class = CommentCreateUpdateSerializer
    serializer_action_classes = {
        "list": CommentSerializer,
        "retrieve": CommentSerializer,
    }
    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_action_classes = {
        "create": (IsUserBanned, IsCommentLocked),
        "update": (IsUserBanned, IsUserTheOwner, IsCommentLocked),
        "partial_update": (IsUserBanned, IsUserTheOwner, IsCommentLocked),
        "destroy": (IsUserBanned, IsUserTheOwner),
    }

    def get_queryset(self):
        queryset = Comment.objects.prefetch_related("children").all()

        if self.action == "list":
            queryset = queryset.filter(parent__isnull=True)

        return queryset

    def get_serializer(self, *args, **kwargs):
        exclude = []

        if self.action in ["list", "retrieve"]:
            children = self.request.query_params.get("children", False)
            if children is False:
                exclude += ["children"]

        kwargs["exclude"] = exclude
        return super().get_serializer(*args, **kwargs)
