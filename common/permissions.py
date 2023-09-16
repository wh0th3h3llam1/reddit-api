from rest_framework.permissions import IsAuthenticatedOrReadOnly

from post.models import Comment
from subreddit.models import SubredditUser


class IsSubredditOwnerOrModerator(IsAuthenticatedOrReadOnly):
    message = "Not allowed"

    def has_permission(self, request, view):
        return False
        # if super().has_permission(request, view):
        #     path = list(filter(lambda x: x, request.stream.path.split("/")))


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
            return not is_thread_locked
        return False


class IsUserTheOwner(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            return obj.user == request.user
        return False
