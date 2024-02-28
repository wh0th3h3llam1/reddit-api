from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from common.fields import CurrentModeratorDefault

from common.mixins import SerializerCreateUpdateOnlyMixin
from core.serializers import DynamicFieldsModelSerializer
from subreddit.models import (
    BannedUser,
    Moderator,
    Subreddit,
    SubredditLink,
    SubredditUser,
)
from users.serializers import UserSerializer


class SubredditLinkSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SubredditLink
        fields = ("id", "subreddit", "name", "url")


class ModeratorSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer(fields=("id", "username"))
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Moderator
        fields = ("user", "username", "subreddit", "added_by")
        validators = [
            UniqueTogetherValidator(
                queryset=Moderator.objects.all(),
                fields=("user", "subreddit"),
                message="User is already Moderator for the subreddit",
            )
        ]


class SubredditListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Subreddit
        fields = (
            "id",
            "name",
            "display_name",
        )
        read_only_fields = fields


class SubredditDetailSerializer(DynamicFieldsModelSerializer):
    owner = UserSerializer(fields=("id", "username"))
    moderators_count = serializers.IntegerField(
        source="moderators.count", read_only=True
    )
    moderators = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_links(self, instance: Subreddit):
        return SubredditLinkSerializer(
            instance.links.all(), exclude=("subreddit",), many=True
        ).data

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_moderators(self, instance: Subreddit):
        return ModeratorSerializer(
            instance.moderators.all(),
            many=True,
            read_only=True,
            fields=("username",),
        ).data

    def get_joined(self, instance: Subreddit) -> bool:
        user = self.context.get("request").user
        if user.is_authenticated:
            return instance.joined_users.filter(user=user).exists()
        return False

    class Meta:
        model = Subreddit
        fields = (
            "owner",
            "name",
            "display_name",
            "description",
            "about",
            "nsfw",
            "image",
            "cover_picture",
            "moderators_count",
            "moderators",
            "links",
            "joined",
            "created",
        )
        read_only_fields = fields


class SubredditCreateUpdateSerializer(
    SerializerCreateUpdateOnlyMixin, DynamicFieldsModelSerializer
):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    links = serializers.ListField(
        required=False, allow_empty=False, write_only=True
    )

    class Meta:
        model = Subreddit
        fields = "__all__"
        create_only_fields = ("name",)
        update_only_fields = ("links",)

    def create(self, validated_data):
        validated_data.pop("links", None)
        # self._validate_subreddit_links(subreddit_links)

        instance = super().create(validated_data)

        # add_link_to_subreddit(
        #     subreddit=instance, links=subreddit_links, update_or_create=False
        # )

        return instance

    def update(self, instance, validated_data: dict):
        subreddit_links: list = validated_data.pop("links", [])
        self._validate_subreddit_links(subreddit_links)

        instance = super().update(instance, validated_data)

        add_link_to_subreddit(
            subreddit=instance, links=subreddit_links, update_or_create=True
        )

        return instance

    def _validate_subreddit_links(self, links: list):
        if not links:
            return

        serializer = SubredditLinkSerializer(
            data=links, exclude=("subreddit",), many=True
        )
        serializer.is_valid(raise_exception=True)


class SubredditUserSerializer(DynamicFieldsModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SubredditUser
        fields = ("user", "subreddit")
        validators = [
            UniqueTogetherValidator(
                queryset=SubredditUser.objects.all(),
                fields=("user", "subreddit"),
                message="You already joined the subreddit",
            )
        ]


class BannedUserSerializer(DynamicFieldsModelSerializer):

    banned_by = serializers.HiddenField(default=CurrentModeratorDefault())

    class Meta:
        model = BannedUser
        fields = (
            "user",
            "subreddit",
            "description",
            "banned_until",
            "banned_by",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=BannedUser.objects.all(),
                fields=("user", "subreddit"),
                message="User already banned",
            )
        ]

    def create(self, validated_data):
        instance, _ = BannedUser.objects.get_or_create(**validated_data)

        return instance


def add_link_to_subreddit(
    subreddit: Subreddit, links: list, update_or_create=False
) -> None:
    if update_or_create is True:
        for link in links:
            SubredditLink.objects.update_or_create(subreddit=subreddit, **link)
    else:
        for link in links:
            SubredditLink.objects.create(subreddit=subreddit, **link)
