from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notes.models import Note


@receiver(post_delete, sender=Note, dispatch_uid="1122")
def create_note(sender, instance, created, **kwargs):
    print("Note created")
