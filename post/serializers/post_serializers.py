from uuid import uuid4
from django.utils.text import slugify

from rest_framework import serializers

from common.mixins import SerializerCreateUpdateOnlyMixin
from core.serializers import DynamicFieldsModelSerializer
from post.models import Post
from subreddit.serializers import SubredditListSerializer
from users.serializers import UserSerializer

# Create your serializers here.


class PostListSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer(fields=("id", "username"))
    subreddit = SubredditListSerializer()

    class Meta:
        model = Post
        fields = (
            "user",
            "subreddit",
            "title",
            "body",
            "slug",
            "post_type",
            "locked",
            "created",
        )


class PostDetailSerializer(DynamicFieldsModelSerializer):
    # comments = serializers.SerializerMethodField()
    post_type_display = serializers.CharField(
        source="get_post_type_display", read_only=True
    )
    slug = serializers.ReadOnlyField()
    user = UserSerializer(fields=("id", "username"))

    # def get_comments(self, instance: Post):
    #     return CommentSerializer(
    #         instance.comments.filter(parent__isnull=True), many=True
    #     ).data

    class Meta:
        model = Post
        fields = (
            "id",
            "slug",
            "title",
            "body",
            "post_type",
            "post_type_display",
            "edited",
            "locked",
            "last_locked_at",
            "last_locked_by",
            "user",
            "subreddit",
            # "comments",
        )


class PostCreateUpdateSerializer(
    SerializerCreateUpdateOnlyMixin, DynamicFieldsModelSerializer
):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs: dict):
        attrs.pop("slug", None)

        if self.instance is None:
            title = attrs.get("title", None)

            slug = slugify(title)
            if self.Meta.model.objects.filter(slug=slug).exists():
                while True:
                    random = uuid4().hex[:6]
                    if self.Meta.model.objects.filter(
                        slug=f"{slug}_{random}"
                    ).exists():
                        continue
                    else:
                        slug += f"_{random}"
                        break
            attrs["slug"] = slug

        return attrs

    class Meta:
        model = Post
        fields = ("user", "title", "body", "subreddit", "post_type")
        create_only_fields = ("title", "slug")
