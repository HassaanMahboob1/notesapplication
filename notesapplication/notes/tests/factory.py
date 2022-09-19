from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from notes.models import Note


class NoteFactory(DjangoModelFactory):
    """Factory class to create Notes."""

    class Meta:
        model = Note

    date_created = timezone.now()
    date_updated = timezone.now()
    title = FuzzyText(length=10)
    text = FuzzyText(length=10)
