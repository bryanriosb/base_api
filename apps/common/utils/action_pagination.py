from functools import wraps
from django.db.models import QuerySet
from rest_framework.response import Response


def paginate(get_serializer=None):
    """Make sure that your action returns a list or QuerySet when using this decorator."""
    def pagination(func):
        try:
            @wraps(func)
            def inner(self, *args, **kwargs):
                queryset = func(self, *args, **kwargs)
                assert isinstance(queryset, (list, QuerySet)), "apply_pagination expects a List or a QuerySet"

                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True) \
                        if not get_serializer else get_serializer(page, many=True, context={'request': self.request})
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(queryset, many=True, context={'request': self.request})
                return Response(serializer.data)

            return inner
        except Exception as e:
            raise ValueError(e)
    return pagination
