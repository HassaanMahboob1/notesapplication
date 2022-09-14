from notes.api_v1.permissions import SuperUserReadOnly
from notes.models import Comment
from notes.models import Note
from notes.models import NoteVersion
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .pagination import CustomPagination
from .serializers import CommentSerializer
from .serializers import NoteCommentSerializer
from .serializers import NotesSerializer


class NotesViewSet(viewsets.ModelViewSet):
    """
    NotesViewset: API endpoints for Note functionality
    URL : /Notes/
    METHOD : POST , GET , PATCH , DELETE
    """

    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated, SuperUserReadOnly)
    serializer_class = NoteCommentSerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ["text"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NoteCommentSerializer
        return NotesSerializer

    def get_queryset(self):
        queryset = Note.objects.all()
        is_shared = self.request.query_params.get("is_shared")
        is_archive = self.request.query_params.get("is_archive")

        current_user = self.request.user
        user_notes_queryset = queryset.filter(user=current_user, archive=0)
        shared_notes_queryset = queryset.filter(sharedwith=current_user)
        queryset = (user_notes_queryset | shared_notes_queryset).distinct()

        if is_archive == "True":
            queryset = Note.objects.all()
            queryset = queryset.filter(user=current_user, archive=1)

        elif is_shared == "True":
            queryset = queryset.filter(sharedwith=current_user)

        return queryset

    serializer = NotesSerializer(queryset, many=True)

    @action(detail=True, methods=["GET"], name="versions")
    def versions(self, request, pk=None):
        """
        Get All versions of a Particular Note endpoint
        """
        queryset = NoteVersion.objects.all()
        queryset = queryset.filter(note_id=pk)
        result_page = CustomPagination.pagination(queryset, request)
        return result_page

    @action(detail=True, methods=["GET"], name="comments")
    def comments(self, request, pk=None):
        """
        Get all comments API endpoint
        """
        queryset = Comment.objects.all()
        queryset = queryset.filter(note_id=pk)
        result_page = CustomPagination.pagination(queryset, request)
        return result_page


class CommentViewSet(viewsets.ModelViewSet):
    """
    CommentViewSet : Update comment viewset
    """

    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset
