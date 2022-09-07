from ast import Not
from dataclasses import field
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..models import Note, NoteVersion, Comment
from datetime import date


class NotesSerializer(serializers.ModelSerializer):
    """
    NotesSerializer : Serializer for Notes and all of its CRUD
                      operations and serializing the data
    """

    class Meta:
        model = Note
        fields = "__all__"

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


class NoteVersionSerializer(serializers.ModelSerializer):
    """
    NotesVersionSerializer : Serializer for Note version and all of operations
                             of versioning
    """

    class Meta:
        model = NoteVersion
        fields = "__all__"


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
