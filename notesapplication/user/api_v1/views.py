from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    """
    RegisterAPIViewSet : Create a new user with the
                        data provided by the user
    URL : /register
    METHOD : POST
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
