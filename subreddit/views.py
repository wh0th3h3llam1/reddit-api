from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from common.mixins.serializer_action_class_mixin import (
    SerializerActionClassMixin,
)

from subreddit.models import Subreddit, SubredditLink
from subreddit.serializers import (
    SubredditCreateUpdateSerializer,
    SubredditDetailSerializer,
    SubredditLinkSerializer,
    SubredditListSerializer,
)

# Create your views here.


@extend_schema(tags=["Subreddit"])
class SubredditViewSet(SerializerActionClassMixin, ModelViewSet):
    queryset = Subreddit.objects.all()
    serializer_class = SubredditCreateUpdateSerializer
    serializer_action_classes = {
        "list": SubredditListSerializer,
        "retrieve": SubredditDetailSerializer,
    }
    lookup_field = "name"

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=["Subreddit Links"],
    parameters=[
        OpenApiParameter(
            "subreddit_name", OpenApiTypes.STR, OpenApiParameter.PATH
        )
    ],
)
class SubredditLinkViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = SubredditLinkSerializer

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
