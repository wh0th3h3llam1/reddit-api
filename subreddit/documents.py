from django_elasticsearch_dsl import Document, fields, Index

from subreddit.models import Subreddit

# Create your documents here.


subreddit_index = Index(name="subreddits")
subreddit_index.settings(number_of_shards=1, number_of_replicas=0)


@subreddit_index.doc_type
class SubredditDocument(Document):
    about_subreddit = fields.TextField()

    class Django:
        model = Subreddit
        fields = (
            "id",
            "name",
            "display_name",
            "description",
        )
