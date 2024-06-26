import uuid

from django.utils import timezone


def get_default_subreddit_image_path() -> str:
    return f"subreddit/default_image.png"


def get_subreddit_image_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit(".", 1)
    file = f"{name.lower().replace(' ', '_')[:48]}_{uuid.uuid4().hex[:8]}.{ext}"
    file_path = f"subreddit/{instance.name}/{file}"
    return file_path


def get_default_subreddit_cover_path() -> str:
    return f"subreddit/default_cover.png"


def get_subreddit_cover_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit(".", 1)
    file = f"{name.lower().replace(' ', '_')[:48]}_{uuid.uuid4().hex[:8]}.{ext}"
    file_path = f"subreddit/{instance.name}/{file}"
    return file_path


def get_default_avatar_path() -> str:
    return f"avatar/default.png"


def get_avatar_path(instance, filename, **kwargs) -> str:
    name, ext = filename.rsplit(".", 1)
    file = f"{name.lower().replace(' ', '_')[:48]}_{uuid.uuid4().hex[:8]}.{ext}"
    file_path = f"avatar/{instance.username}/{file}"
    return file_path


def get_timedelta(days=14) -> timezone.timedelta:
    return timezone.timedelta(days=days)
