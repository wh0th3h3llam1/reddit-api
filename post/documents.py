from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry

from post.models import Post, Comment

# Create your documents here.


post_index = Index(name="posts")

post_index.settings(number_of_shards=1, number_of_replicas=0)


@post_index.doc_type
class PostDocument(Document):
    # id = fields.IntegerField(attr="id")
    # title = fields.TextField(
    #     # attr="title", fields={"suggest": fields.Completion()}
    # )
    # body = fields.TextField()

    class Django:
        model = Post
        fields = ("id", "title", "body")


@registry.register_document
class CommentDocument(Document):
    class Index:
        name = "comments"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Comment
        fields = ("id", "text")
