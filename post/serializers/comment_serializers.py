from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_field,
    extend_schema_serializer,
)
from rest_framework import serializers

from common.mixins import SerializerCreateUpdateOnlyMixin
from core.serializers import DynamicFieldsModelSerializer
from post.models import Comment

# Create your serializers here.


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Example",
            summary="Comments Example",
            description="Includes a `children` field which is nested comments",
            value={
                "children": [
                    {
                        "id": 3,
                        "children": [],
                        "text": "<p>Howdy!</p>",
                        "created": "2023-05-12T08:53:53.170177Z",
                        "modified": "2023-05-12T09:35:13.380617Z",
                        "edited_at": None,
                        "locked": False,
                        "last_locked_at": "2023-05-12T08:53:53Z",
                    }
                ],
            },
            response_only=True,
        )
    ]
)
class CommentSerializer(DynamicFieldsModelSerializer):
    """Retrieve a single comment"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    children = serializers.SerializerMethodField()
    text = serializers.CharField(required=True)

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_children(self, instance: Comment):
        return CommentSerializer(
            instance.children.all(), many=True, read_only=True
        ).data

    class Meta:
        model = Comment
        exclude = (
            # "modified",
            "parent",
            "post",
            "last_locked_by",
            "last_unlocked_at",
            "last_unlocked_by",
        )
        # depth = 3

    # def to_representation(self, instance):
    #     self.fields["children"] = CommentSerializer(
    #         many=True,
    #         read_only=True,
    #     )
    #     return super(CommentSerializer, self).to_representation(instance)


class CommentListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateUpdateSerializer(
    SerializerCreateUpdateOnlyMixin, DynamicFieldsModelSerializer
):
    """Serializer used to create and update a comment"""

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    text = serializers.CharField(required=True)

    def validate(self, attrs: dict) -> dict:
        parent = attrs.get("parent", None)
        post = attrs.get("post")

        if parent is not None:
            if self.instance is not None and parent.id == self.instance.id:
                raise serializers.ValidationError(
                    "Parent comment cannot be same as current"
                )

            if not Comment.objects.filter(id=parent.id, post=post).exists():
                raise serializers.ValidationError(
                    "Parent comment doesn't belong to the Post"
                )

        return attrs

    class Meta:
        model = Comment
        fields = ("id", "user", "parent", "text", "post")
        create_only_fields = ("parent", "post")
