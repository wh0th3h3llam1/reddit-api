from rest_framework.permissions import IsAuthenticatedOrReadOnly

from post.models import Comment, Post
from subreddit.models import SubredditUser


class IsSubredditOwnerOrModerator(IsAuthenticatedOrReadOnly):
    message = "Not allowed"

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            path = list(filter(lambda x: x, request.stream.path.split("/")))


class IsSubredditMember(IsAuthenticatedOrReadOnly):
    message = "Join Subreddit to create a Post"

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            subreddit_id = request.data.get("subreddit", None)

            if subreddit_id is None:
                return False

            return bool(
                SubredditUser.objects.filter(
                    user=request.user, subreddit_id=subreddit_id
                ).exists()
            )

        return False

    def has_object_permission(self, request, view, obj):
        if obj:
            return False
        return


class IsPostLocked(IsAuthenticatedOrReadOnly):
    message = "Cannot edit locked posts"

    def has_object_permission(self, request, view):
        # check if post is locked
        post_id = request.data.get("post", None)
        if post_id is None:
            return False

        try:
            is_post_locked = Post.objects.get(id=post_id).locked
            return False if is_post_locked else True
        except Post.DoesNotExist:
            return False


class IsCommentLocked(IsPostLocked):
    message = "Comment thread is locked"

    # def has_permission(self, request, view):
    #     if super().has_permission(request, view):
    #         # Check if any of the comment is locked

    #         # Check if any of the parent comment is locked

    #         parent_id = request.data.get("parent", None)
    #         if request.method == "POST":
    #             if parent_id is None:
    #                 return True
    #         else:
    #             url_path = list(
    #                 filter(lambda x: x, request.stream.path.split("/"))
    #             )
    #             comment_id = url_path[-1]
    #             comment = Comment.objects.get(id=comment_id)
    #             all_parents = comment.get_all_parents()
    #             parents_lock_status = set(
    #                 list(
    #                     Comment.objects.filter(id__in=all_parents).values_list(
    #                         "locked", flat=True
    #                     )
    #                 )
    #             )

    #             if any(parents_lock_status):
    #                 return False
    #             else:
    #                 return True

    #         return False

    #     return False

    def has_object_permission(self, request, view, obj):
        return False
