from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..models import User, Notes
from datetime import date


class NotesSerializer(serializers.ModelSerializer):
    """
    NotesSerializer : Serializer for Notes and all of its CRUD
                      operations and serializing the data
    """

    class Meta:
        model = Notes
        fields = "__all__"

    def create(self, validated_data):
        note = Notes.objects.create(
            text=validated_data["text"],
            title=validated_data["title"],
            archive=validated_data["archive"],
            date_created=date.today(),
            date_updated=date.today(),
            user=self.context["request"].user,
        )
        note.save()
        return note
