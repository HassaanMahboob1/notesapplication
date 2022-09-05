from django.db import models
from datetime import date
from user.models import User


class Notes(models.Model):
    title = models.CharField(max_length=20, default="", unique=True)
    text = models.CharField(max_length=200)
    date_created = models.DateField(default=str(date.today()))
    date_updated = models.DateField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    archive = models.BooleanField(default=False)
    sharedwith = models.ManyToManyField(User, related_name="shared", blank=True)

    def __str__(self):
        return self.text
