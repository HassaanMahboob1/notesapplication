from django.utils import timezone
from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger
from factory.fuzzy import FuzzyText
from notes.models import Note
from user.models import Users


class UserFactory(DjangoModelFactory):
    """Factory class to create User objects."""

    class Meta:
        model = Users

    email = Faker("safe_email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    username = Faker("name")
