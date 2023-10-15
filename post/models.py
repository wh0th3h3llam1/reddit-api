from __future__ import annotations
from typing import TYPE_CHECKING
from django.contrib.contenttypes.fields import GenericRelation

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_lifecycle import BEFORE_CREATE, LifecycleModelMixin, hook

from common.choices import POST_TYPES
from core.models import BaseModel
from subreddit.models import Moderator, Subreddit
from users.models import User  # , Saved

if TYPE_CHECKING:
    from django.db.models import Manager

# Create your models here.

# https://hub.steampipe.io/plugins/turbot/reddit/tables/reddit_my_comment


class Post(BaseModel):
    user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="posts", null=True
    )
    subreddit = models.ForeignKey(
        to=Subreddit, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    slug = models.SlugField(
        verbose_name=_("Post Slug"), max_length=250, unique=True
    )

    post_type = models.CharField(max_length=8, choices=POST_TYPES)

    edited = models.DateTimeField(blank=True, null=True)

    locked = models.BooleanField(
        verbose_name=_("Is Post locked?"), default=False
    )
    last_locked_by = models.ForeignKey(
        to=Moderator,
        on_delete=models.SET_NULL,
        related_name="locked_posts",
        blank=True,
        null=True,
    )
    last_locked_at = models.DateTimeField(blank=True, null=True)

    last_unlocked_by = models.ForeignKey(
        to=Moderator,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    last_unlocked_at = models.DateTimeField(blank=True, null=True)

    # saved = GenericRelation(to=Saved, related_query_name="saved_posts")

    # pinned: Manager["PinnedPost"]
    # pinned_comments: Manager["PinnedComment"]
    comments: Manager["Comment"]

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self) -> str:
        return f"{self.slug}"


class Comment(LifecycleModelMixin, BaseModel):
    user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="comments", null=True
    )
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name="comments"
    )

    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
    )
    text = models.TextField()

    edited_at = models.DateTimeField(
        verbose_name=_("Comment edited at"), blank=True, null=True
    )
    locked = models.BooleanField(
        verbose_name=_("Is thread locked?"), default=False
    )
    last_locked_by = models.ForeignKey(
        to=Moderator,
        on_delete=models.SET_NULL,
        related_name="locked_comments",
        blank=True,
        null=True,
    )
    last_locked_at = models.DateTimeField(blank=True, null=True)

    last_unlocked_by = models.ForeignKey(
        to=Moderator,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    last_unlocked_at = models.DateTimeField(blank=True, null=True)

    # saved = GenericRelation(to=Saved, related_query_name="saved_comments")

    # pinned: Manager["PinnedComment"]
    children: Manager["Comment"]

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self) -> str:
        return f"{self.post.subreddit} || {self.post} - {self.id}"

    @hook(hook=BEFORE_CREATE)
    def post_after_create(self) -> None:
        if self.post.subreddit.comments_locked_by_default is True:
            self.locked = True
            self.locked_at = timezone.now()

    def get_all_parents(self) -> list[int]:
        comments = []
        comment = self
        comments.append(self.pk)
        while True:
            if comment.parent is None:
                break
            comments.append(comment.parent.id)
            comment = comment.parent

        return comments


# class PinnedPost(BaseModel):
#     subreddit = models.ForeignKey(
#         to=Subreddit, on_delete=models.CASCADE, related_name="pinned_posts"
#     )
#     post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="pinned")
#     pinned_by = models.ForeignKey(
#         to=Moderator,
#         on_delete=models.SET_NULL,
#         related_name="pinned_posts",
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         verbose_name = _("Pinned Post")
#         verbose_name_plural = _("Pinned Posts")


# class PinnedComment(BaseModel):
#     post = models.ForeignKey(
#         to=Post, on_delete=models.CASCADE, related_name="pinned_comments"
#     )
#     comment = models.ForeignKey(
#         to=Comment, on_delete=models.CASCADE, related_name="pinned"
#     )
#     pinned_by = models.ForeignKey(
#         to=Moderator,
#         on_delete=models.SET_NULL,
#         related_name="pinned_comments",
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         verbose_name = _("Pinned Comment")
#         verbose_name_plural = _("Pinned Comments")


# class ReportedPost(BaseModel):
#     user = models.ForeignKey(
#         to=User, on_delete=models.SET_NULL, related_name="reported_posts", null=True
#     )
#     post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="reported")
#     reason = models.CharField()

#     class Meta:
#         verbose_name = _("Reported Post")
#         verbose_name_plural = _("Reported Posts")
