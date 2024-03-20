# Generated by Django 4.2.4 on 2024-02-10 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("subreddit", "0007_alter_subreddituser_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="BannedUser",
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
                ("description", models.TextField(blank=True, null=True)),
                ("banned_until", models.DateTimeField(blank=True, null=True)),
                (
                    "banned_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subreddit_users_banned",
                        to="subreddit.moderator",
                    ),
                ),
                (
                    "subreddit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="banned_users",
                        to="subreddit.subreddit",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="banned_subreddits",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Banned User",
                "verbose_name_plural": "Banned Users",
                "unique_together": {("user", "subreddit")},
            },
        ),
    ]
