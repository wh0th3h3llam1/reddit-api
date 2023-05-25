from functools import reduce
import operator
from django.db.models import Q

from django.shortcuts import get_object_or_404

# https://www.appsloveworld.com/django/100/12/multiple-lookup-fields-for-django-rest-framework
# https://www.appsloveworld.com/django/100/11/django-rest-framework-multiple-lookup-fields
# https://stackoverflow.com/questions/38461366/multiple-lookup-fields-for-django-rest-framework/72770439#72770439
# https://github.com/encode/django-rest-framework/issues/816


class MultipleLookupFieldMixin(object):
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filters = {}

        pk_fields = ["pk", "id"]

        for field in self.lookup_fields:
            identifier = self.kwargs[self.lookup_field]
            if (
                field in pk_fields and identifier.is_digit()
            ) or field not in pk_fields:
                filters[field] = self.kwargs[self.lookup_field]

        q = reduce(operator.or_, (Q(x) for x in filters.items()))
        obj = get_object_or_404(queryset, q)
        self.check_object_permissions(self.request, obj)
        return obj
        # try:
        #     filters[field] = self.kwargs[field]
        # except Exception as err:
        #     print(err)

        return get_object_or_404(queryset, **filters)
