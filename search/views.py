from django.core.exceptions import ValidationError

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from elasticsearch.exceptions import ConnectionError
from elasticsearch_dsl import Q

from post.documents import PostDocument
from post.serializers.post_serializers import PostListSerializer
from subreddit.documents import SubredditDocument
from subreddit.serializers import SubredditListSerializer

# Create your views here.


class SearchView(ListAPIView):
    documents = {"post": PostDocument, "subreddit": SubredditDocument}
    serializer_class = PostListSerializer
    serializer_classes = {
        "post": PostListSerializer,
        "subreddit": SubredditListSerializer,
    }
    _type_choices = ["post", "subreddit", "user", "all"]

    def get_queryset(self):
        search_term = self.request.query_params.get("query", None)
        if search_term is None:
            raise ValidationError("`query` is required")
        typee = self.request.query_params.get("type", "post").lower()

        if typee not in self._type_choices:
            raise ValidationError(
                f"`type` is invalid. Choices are {', '.join(self._type_choices)}"
            )

        if typee == "post":
            queryset = (
                PostDocument.search()
                .query(
                    Q(
                        name_or_query="multi_match",
                        query=search_term,
                        fields=["title", "slug", "body"],
                    )
                )
                .to_queryset()
            )
        elif typee == "subreddit":
            queryset = (
                self.documents[typee]
                .search()
                .filter(
                    "term",
                    name=search_term,
                    display_name=search_term,
                    description=search_term,
                    about=search_term,
                )
                .to_queryset()
            )

        # elif typee == "all":
        #     queryset =

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except ValidationError as err:
            return Response(
                {"message": err.message}, status=HTTP_400_BAD_REQUEST
            )
        except ConnectionError as err:
            return Response(
                {
                    "message": "Contact Admin with mentioned code",
                    "code": "elasticsearch_error",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
