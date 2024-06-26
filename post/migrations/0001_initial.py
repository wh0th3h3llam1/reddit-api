# Generated by Django 4.2.1 on 2023-05-11 09:15

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("subreddit", "0003_alter_moderator_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("body", ckeditor.fields.RichTextField(blank=True, null=True)),
                (
                    "slug",
                    models.SlugField(
                        editable=False, unique=True, verbose_name="Post Slug"
                    ),
                ),
                (
                    "post_type",
                    models.CharField(
                        choices=[
                            ("text", "Text"),
                            ("image", "Image"),
                            ("video", "Video"),
                            ("link", "Link"),
                        ],
                        max_length=8,
                    ),
                ),
                ("edited", models.DateTimeField(blank=True, null=True)),
                (
                    "locked",
                    models.BooleanField(default=False, verbose_name="Is Post locked?"),
                ),
                ("locked_at", models.DateTimeField(blank=True, null=True)),
                ("unlocked_at", models.DateTimeField(blank=True, null=True)),
                (
                    "last_locked_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="locked_posts",
                        to="subreddit.moderator",
                    ),
                ),
                (
                    "last_unlocked_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="subreddit.moderator",
                    ),
                ),
                (
                    "subreddit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to="subreddit.subreddit",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("text", ckeditor.fields.RichTextField()),
                (
                    "edited_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Post edited at"
                    ),
                ),
                (
                    "locked",
                    models.BooleanField(
                        default=False, verbose_name="Is thread locked?"
                    ),
                ),
                ("locked_at", models.DateTimeField(blank=True, null=True)),
                ("unlocked_at", models.DateTimeField(blank=True, null=True)),
                (
                    "locked_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="locked_comments",
                        to="subreddit.moderator",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_comments",
                        to="post.comment",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="post.post",
                    ),
                ),
                (
                    "unlocked_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="subreddit.moderator",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
    ]
