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
from notes.models import Notes
from notes.api_v1.filters import ArchiveFilter


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = NotesSerializer

    def list(self, request):
        """
        list : List the notes to the user of its own
        URL : /Notes/
        METHOD : POST
        Request Data :
                request url with users Access Token
        Response Data :
            {
                "model": "notes.notes",
                "pk": 31,
                "fields": {
                    "title": "Note 6",
                    "text": "sixth-Party",
                    "date_created": "2022-09-02",
                    "date_updated": "2022-09-02",
                    "user": 4,
                    "archive": false,
                    "sharedwith": []
                }
            }
        """
        queryset = Notes.objects.all()
        user = request.user
        queryset = queryset.filter(user=user, archive=0)
        serializer = NotesSerializer(queryset, many=True)
        return Response(serializer.data)


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    permission_classes = [
        SuperUserReadOnly,
    ]
    serializer_class = NotesSerializer
    # filter_backends = (ArchiveFilter,)
    # filterset_fields = ('archive',)

    def list(self, request):
        """
        list : List the Archive notes to the user
        URL : /archive?archive=True
        METHOD : POST
        Request Data :
                request url with users Access Token
        """
        queryset = Notes.objects.all()
        user = request.user
        queryset = queryset.filter(user=user, archive=1)
        serializer = NotesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        post : Archive the notes from the list of the notes
                written by user
        URL : /archive/{{noteid}}/
        METHOD : POST
        Request data :
            request the url with users Access token
        """
        queryset = Notes.objects.all()
        queryset = queryset.filter(pk=kwargs["pk"])
        queryset.update(archive=1)
        serializer = NotesSerializer(queryset, many=True)
        return Response(serializer.data)

    # def filter_queryset(self, queryset):
    #     filter_backends = (DjangoFilterBackend, )
    #     for backend in list(filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset, view=self)
    #     return queryset


@api_view(["GET", "PATCH"])
def shared(request):
    """
    shared : List out the notes which are shared with the
            current logged in user by the others
    URL : /shared
    METHOD : POST
    Request data :
        request the url with users Access token
    """
    queryset = Notes.objects.all()
    current_user = request.user.id
    queryset = queryset.filter(sharedwith=current_user)
    serializer = NotesSerializer(queryset, many=True)
    return Response(serializer.data)
