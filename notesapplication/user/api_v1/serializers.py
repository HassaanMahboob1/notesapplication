from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..models import Users


class RegisterSerializer(serializers.ModelSerializer):
    """
    RegisterSerializer : Serializer for registering new user and
                        serializing the data
    """

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    username = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = "__all__"
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user_obj = Users.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            username=validated_data["username"],
            last_name=validated_data["last_name"],
        )
        user_obj.set_password(validated_data["password"])
        user_obj.save()
        return user_obj
