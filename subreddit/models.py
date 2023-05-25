from __future__ import annotations
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from django_lifecycle import AFTER_CREATE, LifecycleModelMixin, hook

from common.constants import FieldConstants
from common.utils import (
    get_default_subreddit_cover_path,
    get_default_subreddit_image_path,
    get_subreddit_cover_path,
    get_subreddit_image_path,
)
from core.models import BaseModel
from users.models import User

# from tag.models import Flair, Topic

if TYPE_CHECKING:
    from django.db.models import Manager

# Create your models here.


class Subreddit(LifecycleModelMixin, BaseModel):
    owner = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name="owned_subreddits"
    )
    name = models.CharField(
        max_length=FieldConstants.MAX_VALUE_LENGTH, unique=True
    )
    display_name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH)
    description = models.TextField()
    about = RichTextField(blank=True, null=True)

    nsfw = models.BooleanField(
        verbose_name=_("NSFW Posts only?"), default=False
    )

    max_pinned_posts = models.PositiveSmallIntegerField(default=3)
    max_pinned_comments = models.PositiveSmallIntegerField(default=2)

    comments_locked_by_default = models.BooleanField(
        verbose_name=_("Are Post comments locked by default?"), default=False
    )

    image = models.ImageField(
        upload_to=get_subreddit_image_path,
        default=get_default_subreddit_image_path,
    )
    cover_picture = models.ImageField(
        upload_to=get_subreddit_cover_path,
        default=get_default_subreddit_cover_path,
    )

    # flairs = models.ManyToManyField(
    #     to=Flair, verbose_name="Flairs", related_name="subreddits",
    # )
    # topics = models.ManyToManyField(
    #     to=Topic, verbose_name="Topics", related_name="subreddits"
    # )
    # moderators = models.ManyToManyField(to=User, through="Moderator")

    moderators: Manager["Moderator"]
    links: Manager["SubredditLink"]
    posts: Manager["Post"]

    class Meta:
        verbose_name = _("Subreddit")
        verbose_name_plural = _("Subreddits")

    def __str__(self) -> str:
        return f"{self.name}"

    @hook(hook=AFTER_CREATE)
    def add_owner_as_mod(self) -> None:
        SubredditUser.objects.create(user=self.owner, subreddit=self)
        Moderator.objects.create(user=self.owner, subreddit=self)


class SubredditUser(BaseModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="joined_subreddits"
    )
    subreddit = models.ForeignKey(
        to=Subreddit, on_delete=models.CASCADE, related_name="joined_users"
    )

    class Meta:
        verbose_name = "Subreddit User"
        verbose_name_plural = "Subreddit Users"


class Moderator(BaseModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="moderating_subreddits"
    )
    subreddit = models.ForeignKey(
        to=Subreddit, on_delete=models.CASCADE, related_name="moderators"
    )
    added_by = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        related_name="invited_moderators",
        blank=True,
        null=True,
    )

    invited_moderators: Manager["Moderator"]

    class Meta:
        verbose_name = _("Moderator")
        verbose_name_plural = _("Moderators")
        unique_together = ("user", "subreddit")

    def __str__(self) -> str:
        return f"{self.user} - {self.subreddit}"


class SubredditLink(BaseModel):
    subreddit = models.ForeignKey(
        to=Subreddit, on_delete=models.CASCADE, related_name="links"
    )
    name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH)
    url = models.URLField(verbose_name=_("URL"))

    class Meta:
        verbose_name = _("Subreddit Link")
        verbose_name_plural = _("Subreddit Links")
        unique_together = ("subreddit", "name")

    def __str__(self) -> str:
        return f"{self.subreddit.name} || {self.name} - {self.url}"


# class BannedSubredditUser(BaseModel):
#     user = models.ForeignKey(
#         to=User, on_delete=models.CASCADE, related_name="banned_subreddits"
#     )
#     subreddit = models.ForeignKey(
#         to=Subreddit, on_delete=models.CASCADE, related_name="banned_users"
#     )
#     banned = models.BooleanField(verbose_name=_("Is user banned?"), default=False)
#     note = models.TextField(blank=True, null=True)
#     banned_till = models.DateTimeField()
#     #! TODO Add appropriate `to` & `related_name` field
#     banned_by = models.ForeignKey(
#         to=Moderator,
#         on_delete=models.SET_NULL,
#         related_name="subreddit_users_banned",
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         verbose_name = _("Banned Subreddit User")
#         verbose_name_plural = _("Banned Subreddit Users")
