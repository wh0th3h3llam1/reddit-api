from uuid import uuid4
from django.utils.text import slugify

from post.models import Post


def make_post_slug(title: str) -> str:
    slug = slugify(title)
    if Post.objects.filter(slug=slug).exists():
        while True:
            random_slug = f"{slug}_{uuid4().hex[:6]}"

            if Post.objects.filter(slug=random_slug).exists():
                continue
            else:
                slug = random_slug
                break

    return slug
