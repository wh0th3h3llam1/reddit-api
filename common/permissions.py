from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from post.models import Comment
from subreddit.models import BannedUser, SubredditUser
from users.models.user import User


class IsSubredditOwnerOrModerator(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            return request.user.id in obj.moderators.select_related(
                "user"
            ).values_list("user__id", flat=True)
        return False


class IsSubredditMember(IsAuthenticatedOrReadOnly):
    message = "Join Subreddit to create a Post"

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            subreddit = request.path.rsplit("/api/r/")[-1].split("/")[0]

            if not subreddit:
                return False

            return bool(
                SubredditUser.objects.filter(
                    user=request.user, subreddit__name=subreddit
                ).exists()
            )

        return False


class IsPostLocked(IsAuthenticatedOrReadOnly):
    message = "Cannot edit locked posts"

    def has_object_permission(self, request, view, obj):
        # check if post is locked
        if super().has_object_permission(request, view, obj):
            return bool(not obj.locked)
        return False


class IsCommentLocked(IsAuthenticatedOrReadOnly):
    message = "Comment thread is locked"

    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            parents = obj.get_all_parents()
            is_thread_locked = Comment.objects.filter(
                id__in=parents, locked=True
            ).exists()
            return bool(not is_thread_locked)
        return False


class IsUserTheOwner(IsAuthenticatedOrReadOnly):
    message = "You are not allowed to perform this action"

    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            if hasattr(obj, "user"):
                return obj.user == request.user
            if hasattr(obj, "owner"):
                return obj.owner == request.user
            if isinstance(obj, User):
                return obj == request.user
        return False


class IsUserBanned(IsAuthenticatedOrReadOnly):
    message = "You are banned from interacting in this subreddit"

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            subreddit = request.path.rsplit("/api/r/")[-1].split("/")[0]

            if not subreddit:
                return False

            banned_user = BannedUser.objects.filter(
                user=request.user, subreddit__name=subreddit
            ).first()
            if banned_user and banned_user.banned_until > timezone.now():
                return False
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            return bool(not obj.banned_users.filter(user=request.user).exists())
        return False
