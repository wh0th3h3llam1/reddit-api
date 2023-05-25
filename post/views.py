from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from common.mixins import (
    SerializerActionClassMixin,
    PermissionActionClassMixin,
)
from common.permissions import (
    IsCommentLocked,
    IsPostLocked,
    IsSubredditMember,
    IsSubredditOwnerOrModerator,
)
from post.models import Comment, Post
from post.serializers import (
    CommentSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
)

# Create your views here.


@extend_schema(tags=["Posts"])
class PostViewSet(
    # MultipleLookupFieldMixin,
    PermissionActionClassMixin,
    SerializerActionClassMixin,
    ModelViewSet,
):
    serializer_class = PostCreateUpdateSerializer
    serializer_action_classes = {
        "list": PostDetailSerializer,
        "retrieve": PostDetailSerializer,
    }
    lookup_field = "slug"
    # lookup_fields = ("slug", "id", "pk")
    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_action_classes = {
        # "create": (IsSubredditMember,),
        "update": ((IsPostLocked | IsSubredditOwnerOrModerator),),
        "partial_update": ((IsPostLocked | IsSubredditOwnerOrModerator),),
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
            exclude += (
                "subreddit",
                "comments",
            )
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


@extend_schema(tags=["Comments"])
class CommentViewSet(PermissionActionClassMixin, ModelViewSet):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_action_classes = {
        "create": ((IsCommentLocked | IsSubredditMember),),
        "update": (IsCommentLocked,),
        "partial_update": (IsCommentLocked,),
    }
