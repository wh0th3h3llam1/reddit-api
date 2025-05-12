from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from common.mixins import PermissionActionClassMixin, SerializerActionClassMixin
from common.permissions import (
    IsSubredditOwnerOrModerator,
    IsUserBanned,
    IsUserTheOwner,
)
from subreddit.filters import SubredditFilterSet
from subreddit.models import Subreddit, SubredditLink
from subreddit.serializers import (
    BannedUserDetailSerializer,
    BannedUserSerializer,
    SubredditCreateUpdateSerializer,
    SubredditDetailSerializer,
    SubredditLinkSerializer,
    SubredditListSerializer,
    SubredditUserSerializer,
    UnbanUserSerializer,
)

# Create your views here.


@extend_schema(tags=["Subreddit"])
class SubredditViewSet(
    PermissionActionClassMixin, SerializerActionClassMixin, ModelViewSet
):
    """Subreddit ViewSet"""

    serializer_class = SubredditCreateUpdateSerializer
    serializer_action_classes = {
        "list": SubredditListSerializer,
        "retrieve": SubredditDetailSerializer,
        "join": SubredditUserSerializer,
        "bans": BannedUserDetailSerializer,
        "ban": BannedUserSerializer,
        "unban": UnbanUserSerializer,
    }
    permission_action_classes = {
        "update": ((IsUserTheOwner | IsSubredditOwnerOrModerator),),
        "partial_update": ((IsUserTheOwner | IsSubredditOwnerOrModerator),),
        "destroy": (IsUserTheOwner,),
        "join": (IsUserBanned,),
        "bans": (IsSubredditOwnerOrModerator,),
        "ban": (IsSubredditOwnerOrModerator,),
        "unban": (IsSubredditOwnerOrModerator,),
    }
    lookup_field = "name"
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubredditFilterSet
    search_fields = ["name"]

    def get_queryset(self):
        queryset = Subreddit.objects.all()
        if self.action == ["retrieve"]:
            queryset = queryset.prefetch_related(
                "joined_users", "links", "moderators"
            )
        elif self.action in ["partial_update", "update"]:
            queryset = queryset.prefetch_related("links")
        elif self.action in ["bans", "ban", "unban"]:
            queryset = queryset.prefetch_related("banned_users")
        return queryset

    @action(methods=["POST"], detail=True)
    def join(self, request, *args, **kwargs):
        """Allow a user to join subreddit"""

        msg = "You already joined the subreddit"
        serializer = self.get_serializer(
            data={"subreddit": self.get_object().id}
        )
        data = {"message": "Joined Subreddit"}
        if serializer.is_valid():
            serializer.save()
        else:
            if msg in serializer.errors.get("non_field_errors", []):
                data = {"message": msg}
            else:
                data = serializer.errors

        return Response(data=data, status=HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def bans(self, request, *args, **kwargs):
        """Allow moderators to see all banned user"""

        banned_users = self.get_object().banned_users.select_related(
            "user", "banned_by"
        )
        serializer = self.get_serializer(
            banned_users, exclude=("subreddit",), many=True
        )
        return Response(data=serializer.data, status=HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def ban(self, request, *args, **kwargs):
        """Allow moderators to ban user"""

        msg = "User already banned"
        status = HTTP_200_OK
        serializer = self.get_serializer(
            data={"subreddit": self.get_object().id, **request.data}
        )
        data = {"message": "User banned"}
        if serializer.is_valid():
            serializer.save()
        else:
            if msg in serializer.errors.get("non_field_errors", []):
                data = {"message": msg}
                status = HTTP_400_BAD_REQUEST

        return Response(data=data, status=status)

    @action(methods=["POST"], detail=True)
    def unban(self, request, *args, **kwargs):
        """Allow moderators to unban user"""

        data = {"message": "User unbanned"}
        subreddit = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"subreddit": subreddit}
        )
        serializer.is_valid(raise_exception=True)
        banned_user = get_object_or_404(
            queryset=subreddit.banned_users.all(),
            user__username=serializer.data["user"],
        )
        serializer.save(banned_user=banned_user)
        return Response(data=data, status=HTTP_200_OK)


@extend_schema(
    tags=["Subreddit Links"],
    parameters=[
        OpenApiParameter(
            name="subreddit_name",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True,
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            required=False,
        ),
    ],
)
class SubredditLinkViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """SubredditLink ViewSet"""

    serializer_class = SubredditLinkSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = SubredditLink.objects.select_related("subreddit").filter(
            subreddit__name=self.kwargs["subreddit_name"]
        )
        return queryset

    def get_serializer(self, *args, **kwargs):
        exclude = []
        if self.action == "list":
            exclude += ("subreddit",)

        kwargs["exclude"] = exclude

        return super().get_serializer(*args, **kwargs)
