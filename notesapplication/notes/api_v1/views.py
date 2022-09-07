from pyexpat import model
from django.shortcuts import HttpResponse
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from notes.api_v1.permissions import SuperUserReadOnly
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django_filters.rest_framework import DjangoFilterBackend

from notes.models import NoteVersion, Comment
from .serializers import NotesSerializer, CommentSerializer, NoteVersionSerializer
from notes.models import Note
from notes.api_v1.filters import ArchiveFilter


class NotesViewSet(viewsets.ModelViewSet):
    """
    NotesViewset: API endpoints for Note functionality
    URL : /Notes/
    METHOD : POST , GET , PATCH , DELETE
    """

    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = NotesSerializer

    def get_queryset(self):
        queryset = Note.objects.all()
        user = self.request.user
        is_shared = self.request.query_params.get("is_shared")
        is_archive = self.request.query_params.get("is_archive")

        if is_archive:
            queryset = Note.objects.all()
            user = self.request.user
            queryset = queryset.filter(user=user, archive=1)
            return queryset
        if is_shared is None:
            current_user = self.request.user.id
            queryset1 = queryset.filter(user=user, archive=0)
            queryset2 = queryset.filter(sharedwith=current_user)
            queryset = (queryset1 | queryset2).distinct()
            return queryset
        current_user = self.request.user.id
        queryset = queryset.filter(sharedwith=current_user)
        return queryset

    serializer = NotesSerializer(queryset, many=True)

    @action(detail=True, methods=["GET"], name="versions")
    def versions(self, request, pk=None):
        """
        Get All versions of a Particular Note endpoint
        """
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = NoteVersion.objects.all()
        queryset = queryset.filter(note_id=pk)
        result_page = paginator.paginate_queryset(queryset, request)
        data = NoteVersionSerializer(result_page, many=True)
        return paginator.get_paginated_response(data.data)

    @action(detail=True, methods=["GET"], name="comments")
    def comments(self, request, pk=None):
        """
        Get all comments API endpoint
        """
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = Comment.objects.all()
        queryset = queryset.filter(note_id=pk)
        result_page = paginator.paginate_queryset(queryset, request)
        data = NoteVersionSerializer(result_page, many=True)
        return paginator.get_paginated_response(data.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CommentViewSet : Update comment viewset
    """

    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        note_id = self.request.query_params.get("note_id")
        queryset = Comment.objects.all()
        return queryset
