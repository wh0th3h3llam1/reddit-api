from django.utils import timezone

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.serializers import DynamicFieldsModelSerializer
from users.models import User

# Create your serializers here.


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Token
        fields = ("key", "username", "user")


class UserSerializer(DynamicFieldsModelSerializer):
    date_joined = serializers.DateTimeField(source="created")

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "date_joined")


class UserDetailSerializer(DynamicFieldsModelSerializer):
    date_joined = serializers.DateTimeField(source="created")
    posts = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_posts(self, instance: User) -> dict:
        from post.serializers.post_serializers import PostListSerializer

        return PostListSerializer(
            instance=instance.posts.all(),
            many=True,
            read_only=True,
            fields=(
                "subreddit",
                "title",
                "body",
                "slug",
                "edited_at",
                "locked",
            ),
        ).data

    def get_comments(self, instance: User) -> dict:
        from post.serializers.comment_serializers import CommentListSerializer

        return CommentListSerializer(
            instance=instance.comments.all(),
            many=True,
            read_only=True,
            fields=("post", "text", "edited_at", "locked"),
        ).data

    class Meta:
        model = User
        fields = ("username", "avatar", "date_joined", "posts", "comments")


class UserUpdateSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
        )


class ChangeUsernameSerializer(serializers.ModelSerializer):
    confirm = serializers.BooleanField(required=False, default=False)
    username_last_changed = serializers.HiddenField(default=timezone.now())

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username not available")
        return username

    def validate_confirm(self, confirm: bool):
        if confirm is False:
            raise serializers.ValidationError("Confirm username change")
        return confirm

    def validate(self, attrs):
        last_changed = self.instance.username_last_changed

        if (
            last_changed is not None
            and last_changed > timezone.now() - timezone.timedelta(days=14)
        ):
            raise serializers.ValidationError(
                "You can't change username for at least 14 days after changing once."
            )
        return attrs

    class Meta:
        model = User
        fields = ("username", "confirm", "username_last_changed")


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = ("avatar",)
