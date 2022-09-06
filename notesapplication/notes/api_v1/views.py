from django.shortcuts import HttpResponse
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from notes.api_v1.permissions import SuperUserReadOnly
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import NotesSerializer
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
            queryset = queryset.filter(user=user, archive=0)
            return queryset
        current_user = self.request.user.id
        queryset = queryset.filter(sharedwith=current_user)
        return queryset

    serializer = NotesSerializer(queryset, many=True)
