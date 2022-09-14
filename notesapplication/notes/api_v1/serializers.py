from rest_framework import serializers

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
        request = self.context.get("request", None)
        if request.user:
            comment = Comment.objects.create(
                text=validated_data["text"],
                note=validated_data["note"],
                user=request.user,
            )
            comment.save()
            return comment
        else:
            raise serializers.ValidationError("User does not exists")


class NotesSerializer(serializers.ModelSerializer):
    """
    NotesSerializer : Serializer for Notes and all of its CRUD
                      operations and serializing the data
    """

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        note = Note.objects.create(
            text=validated_data["text"],
            title=validated_data["title"],
            archive=validated_data["archive"],
            user=self.context["request"].user,
        )
        note.save()
        return note

    def update(self, instance, validated_data):
        request = self.context.get("request", None)
        note_version = NoteVersion.objects.create(
            note=instance,
            edited_by=request.user,
            title=instance.title,
            text=instance.text,
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        last_comment = instance.comments.last()
        comments = Comment.objects.all()
        if last_comment in comments:
            last_comment_data = CommentSerializer(last_comment).data
            representation["comments"] = last_comment_data
            return representation
        return representation


class NoteCommentSerializer(serializers.ModelSerializer):
    """
    NoteCommentSerializer : Serializer for showing comments with
                            the particular note (when retrieve method is called)
    """

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
