from django_filters.filters import CharFilter
from django_filters.rest_framework import FilterSet

from subreddit.models import Subreddit


class SubredditFilterSet(FilterSet):

    username = CharFilter(method="filter_by_username")

    def filter_by_username(self, queryset, key, value):
        queryset = queryset.filter(
            banned_users__user__username__icontains=value
        )
        return queryset

    class Meta:
        model = Subreddit
        fields = ("username",)
