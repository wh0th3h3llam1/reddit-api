# Generated by Django 4.2.1 on 2023-05-27 20:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("subreddit", "0006_alter_subredditlink_url_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="subreddituser",
            unique_together={("user", "subreddit")},
        ),
    ]
