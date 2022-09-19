from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Users class to Register new user and login
    """

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username
