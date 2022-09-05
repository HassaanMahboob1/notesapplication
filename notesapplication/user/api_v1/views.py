from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import RegisterSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    """
    RegisterAPIViewSet : Create a new user with the
                        data provided by the user
    URL : /register
    METHOD : POST
    Request Data :
        {
            "email":"awais.beg@gmail.com",
            "first_name":"awais",
            "last_name":"beg",
            "username":"awaisbeg",
            "password":"awaisbeg123"
        }
    Response Data :
        {
            "id": 4,
            "email": "awais.beg@gmail.com",
            "last_login": null,
            "is_superuser": false,
            "is_staff": false,
            "is_active": true,
            "date_joined": "2022-09-02T10:09:45.054357Z",
            "first_name": "awais",
            "last_name": "beg",
            "groups": [],
            "user_permissions": []
        }
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
