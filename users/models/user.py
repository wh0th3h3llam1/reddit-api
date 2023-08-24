from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework.fields import MinLengthValidator

from phonenumber_field.modelfields import PhoneNumberField

from common.constants import FieldConstants
from common.utils import get_avatar_path, get_default_avatar_path
from common.validators import username_validator
from core.models import BaseModel
from users.managers import UserManager

if TYPE_CHECKING:
    from django.db.models import Manager

# Create your models here.


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name=_("Username"),
        unique=True,
        max_length=FieldConstants.MAX_USERNAME_LENGTH,
        validators=(
            UnicodeUsernameValidator(),
            MinLengthValidator(
                limit_value=5,
                message=_("Username must have at least 5 characters"),
            ),
            username_validator,
        ),
        error_messages={"unique": "Username already taken"},
    )
    email = models.CharField(max_length=100)

    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), blank=True, null=True
    )

    avatar = models.ImageField(
        upload_to=get_avatar_path,
        blank=True,
        default=get_default_avatar_path,
    )

    is_staff = models.BooleanField(
        verbose_name=_("Staff Status"),
        default=False,
        help_text=_("Designate whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        verbose_name=_("Superuser Status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )

    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text="Designates whether this use should be treated as active. "
        "Unselect this instead of deleting accounts (soft delete)",
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    comments: Manager["Comment"]
    emails: Manager["Email"]
    joined_subreddits: Manager["SubredditUser"]
    posts: Manager["Post"]
    moderating_subreddits: Manager["Moderator"]
    owned_subreddits: Manager["Subreddit"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return f"{self.username}"

    def clean(self) -> None:
        self.email = self.__class__.objects.normalize_email(self.email)


class Email(BaseModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="emails"
    )
    email = models.EmailField(max_length=100, unique=True)
    verification_key = models.CharField(
        verbose_name=_("Verification Key"), max_length=48
    )
    verified_at = models.DateTimeField(
        verbose_name=_("Verified At"), blank=True, null=True
    )
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    remote_host = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(
        verbose_name=_("Is this Primary Email?"), default=False
    )

    class Meta:
        verbose_name = _("Email Address")
        verbose_name_plural = _("Email Addresses")

    def __str__(self) -> str:
        return f"{self.user} - {self.email}"

    @property
    def is_verified(self) -> bool:
        return bool(self.verified_at)

    def _set_primary_flags(self) -> None:
        self.user.emails.filter(email=self).update(is_primary=True)
        self.user.emails.exclude(email=self).update(is_primary=False)

    def set_primary(self) -> None:
        self._set_primary_flags()
        self.user.email = self.email
        self.user.save()
