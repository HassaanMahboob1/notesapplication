from django.db.models.signals import post_save
from django.dispatch import receiver
from notes.models import Users


@receiver(post_save, sender=Users, dispatch_uid="1122")
def create_profile(sender, instance, created, **kwargs):
    print("User Created")
