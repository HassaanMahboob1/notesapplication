from dataclasses import fields
from datetime import date
from typing import OrderedDict

from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import UniqueValidator
from user.models import Users

from ..models import Comment
from ..models import Note
from ..models import NoteVersion


class CommentSerializer(serializers.ModelSerializer):
    """
    CommentSerializer : Serializer for comment class and CRUD operations of comments
    """

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        users = Users.objects.all()
        request = self.context.get("request", None)
        if request.user in users:
            comment = Comment.objects.create(
                text=validated_data["text"],
                note_id=validated_data["note_id"],
                user=request.user,
            )
            comment.save()
            return comment
        else:
            raise serializers.ValidationError("User not exists")


class NotesSerializer(serializers.ModelSerializer):
    """
    NotesSerializer : Serializer for Notes and all of its CRUD
                      operations and serializing the data
    """

    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("user",)

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
            date_updated=date.today(),
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        last_comment = instance.comment.last()
        last_comment_data = CommentSerializer(last_comment).data
        representation["comment"] = last_comment_data
        return representation


class NoteCommentSerializer(serializers.ModelSerializer):
    """
    NoteCommentSerializer : Serializer for showing comments with
                            the particular note (when retrieve method is called)
    """

    comment = serializers.SerializerMethodField("paginated_comment")

    class Meta:
        model = Note
        fields = "__all__"


class NoteVersionSerializer(serializers.ModelSerializer):
    """
    NotesVersionSerializer : Serializer for Note version and CRUD operations
                             of versioning
    """

    class Meta:
        model = NoteVersion
        fields = "__all__"
        read_only_fields = ("edited_by",)
