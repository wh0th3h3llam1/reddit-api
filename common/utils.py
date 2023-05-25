import uuid


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


def get_avatar_path(instance, filename, **kwargs) -> str:
    # name, ext
    return
