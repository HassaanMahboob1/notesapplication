from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from ..models import Note, NoteVersion, Comment
from datetime import date

NUMBER_TO_GET_LATEST_COMMENT = 1


class CommentSerializer(serializers.ModelSerializer):
    """
    CommentSerializer : Serializer for comment class and all operations of it
    """

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):

        request = self.context.get("request", None)
        comment = Comment.objects.create(
            text=validated_data["text"],
            note_id=validated_data["note_id"],
            user=request.user,
            date_created=date.today(),
            date_updated=date.today(),
        )
        comment.save()
        return comment


class NotesSerializer(serializers.ModelSerializer):
    """
    NotesSerializer : Serializer for Notes and all of its CRUD
                      operations and serializing the data
    """

    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "text",
            "date_created",
            "date_updated",
            "user",
            "archive",
            "sharedwith",
            "comment",
        ]

    def create(self, validated_data):
        note = Note.objects.create(
            text=validated_data["text"],
            title=validated_data["title"],
            archive=validated_data["archive"],
            date_created=date.today(),
            date_updated=date.today(),
            user=self.context["request"].user,
        )
        note.save()
        return note

    def update(self, instance, validated_data):
        request = self.context.get("request", None)
        note_version = NoteVersion.objects.create(
            note_id=instance,
            edited_by=request.user,
            title=instance.title,
            text=instance.text,
            date_created=date.today(),
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if len(representation["comment"]) > NUMBER_TO_GET_LATEST_COMMENT:
            last_comment = representation["comment"][
                len(representation["comment"]) - NUMBER_TO_GET_LATEST_COMMENT
            ]
            representation["comment"] = []
            representation["comment"].append(last_comment)
        return representation


class NoteCommentSerializer(serializers.ModelSerializer):
    """
    NoteCommentSerializer : Serializer for showing comments with
                            the particular note (when retrieve method is called)
    """

    comment = serializers.SerializerMethodField("paginated_comment")

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "text",
            "date_created",
            "date_updated",
            "user",
            "archive",
            "sharedwith",
            "comment",
        ]

    def paginated_comment(self, obj):
        """
        Class for pagination of a comments
        """
        paginator = PageNumberPagination()
        paginator = Paginator(obj.comment.all(), 10)
        comment = paginator.page(1)
        serializer = CommentSerializer(comment, many=True)
        return serializer.data


class NoteVersionSerializer(serializers.ModelSerializer):
    """
    NotesVersionSerializer : Serializer for Note version and all of operations
                             of versioning
    """

    class Meta:
        model = NoteVersion
        fields = "__all__"
