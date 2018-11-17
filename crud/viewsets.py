import dateutil.parser

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from crud import models, serializers


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TodoViewset(viewsets.ModelViewSet):
    """Viewset for our Todo model."""
    queryset = models.Todo.objects.all()
    ordering = ('-created_at',)
    serializer_class = serializers.TodoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('state',)

    @action(detail=False, methods=['GET'], name='Fetch All')
    def fetch_all(self, request, *args, **kwargs):
        """Fetch all (unpaginated) results.  Reachable at .../fetch_all."""
        queryset = models.Todo.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    dt_format = '\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d+(?:-\d\d:\d\d)?'
    fetch_range_url = r'fetch_by_due_at_range/(?P<start>{0})/(?P<end>{0})'.format(dt_format)

    @action(detail=False, methods=['GET'], name='Fetch By Date Range', url_path=fetch_range_url)
    def fetch_by_due_at_range(self, request, *args, **kwargs):
        """Fetch by newer or older than given datetime."""
        start = dateutil.parser.parse(kwargs['start'])
        end = dateutil.parser.parse(kwargs['end'])
        queryset = models.Todo.objects.filter(due_at__range=[start, end]).all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
