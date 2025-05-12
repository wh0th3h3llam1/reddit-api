import factory

from subreddit.models import Moderator, Subreddit
from users.tests.factories import UserFactory


class Moderator(factory.django.DjangoModelFactory):
    class Meta:
        model = Moderator

    user = UserFactory


class SubredditFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subreddit

    owner = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute()
    display_name = ""
    description = ""
    about = None

    @classmethod
    def _create(self):
        super().create()
