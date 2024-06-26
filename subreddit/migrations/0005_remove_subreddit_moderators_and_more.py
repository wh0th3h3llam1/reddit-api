# Generated by Django 4.2.1 on 2023-05-12 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("subreddit", "0004_alter_subreddit_nsfw"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subreddit",
            name="moderators",
        ),
        migrations.AlterField(
            model_name="moderator",
            name="subreddit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="moderators",
                to="subreddit.subreddit",
            ),
        ),
    ]
