from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from common.mixins import PermissionActionClassMixin, SerializerActionClassMixin
from common.permissions import (
    IsSubredditOwnerOrModerator,
    IsUserBanned,
    IsUserTheOwner,
)
from subreddit.models import Subreddit, SubredditLink
from subreddit.serializers import (
    BannedUserSerializer,
    SubredditCreateUpdateSerializer,
    SubredditDetailSerializer,
    SubredditLinkSerializer,
    SubredditListSerializer,
    SubredditUserSerializer,
)

# Create your views here.


@extend_schema(tags=["Subreddit"])
class SubredditViewSet(
    PermissionActionClassMixin, SerializerActionClassMixin, ModelViewSet
):
    queryset = Subreddit.objects.prefetch_related(
        "banned_users", "joined_users", "links", "moderators"
    ).all()
    serializer_class = SubredditCreateUpdateSerializer
    serializer_action_classes = {
        "list": SubredditListSerializer,
        "retrieve": SubredditDetailSerializer,
        "join": SubredditUserSerializer,
        "ban": BannedUserSerializer,
    }
    permission_action_classes = {
        "update": ((IsUserTheOwner | IsSubredditOwnerOrModerator),),
        "partial_update": ((IsUserTheOwner | IsSubredditOwnerOrModerator),),
        "destroy": (IsUserTheOwner,),
        "join": (IsUserBanned,),
        "ban": (IsSubredditOwnerOrModerator,),
    }
    lookup_field = "name"

    @action(methods=["POST"], detail=True)
    def join(self, request, *args, **kwargs):

        msg = "You already joined the subreddit"
        serializer = self.get_serializer(
            data={"subreddit": self.get_object().id}
        )
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
        else:
            if msg in serializer.errors.get("non_field_errors", []):
                data = {"message": "You already joined the subreddit"}
            else:
                data = serializer.errors

        return Response(data=data, status=HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def ban(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data={"subreddit": self.get_object().id, **request.data}
        )
        data = {"message": "User banned"}
        if serializer.is_valid():
            serializer.save()
        else:
            if "User already banned" in serializer.errors.get(
                "non_field_errors", []
            ):
                data = {"message": "User already banned"}

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
    serializer_class = SubredditLinkSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = SubredditLink.objects.filter(
            subreddit__name=self.kwargs["subreddit_name"]
        )
        return queryset

    def get_serializer(self, *args, **kwargs):
        exclude = []
        if self.action == "list":
            exclude += ("subreddit",)

        kwargs["exclude"] = exclude

        return super().get_serializer(*args, **kwargs)
