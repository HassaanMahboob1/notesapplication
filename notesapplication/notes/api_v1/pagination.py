from notes.api_v1.serializers import NoteVersionSerializer
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination


class CustomPagination(pagination.PageNumberPagination):
    """
    Class for pagination of comments and versions Viewsets
    """

    def pagination(queryset, request, pk=None):
        print("in pagination")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(queryset, request)
        data = NoteVersionSerializer(result_page, many=True)
        return paginator.get_paginated_response(data.data)
