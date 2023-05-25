from typing import Optional
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError("Username must be set")
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(username, password, **kwargs)

    def get_by_natural_key(self, login_field: str | None):
        return self.get(
            Q(username=login_field) | Q(email=login_field) | Q(phone_number=login_field)
        )
