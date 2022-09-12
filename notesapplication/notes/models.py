from datetime import date

from django.db import models
from user.models import Users


class Note(models.Model):
    """
    Note class to perform CRUD operations on Note
    """

    title = models.CharField(
        max_length=39, default="", unique=True, blank=False, null=False
    )
    text = models.CharField(max_length=199)
    date_created = models.DateField(default=str(date.today()))
    date_updated = models.DateField(default="")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)
    sharedwith = models.ManyToManyField(Users, related_name="sharedwith", blank=True)

    def __str__(self):
        return self.text


class NoteVersion(models.Model):
    """
    NoteVersion class to add versions of a note
    """

    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    edited_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=39, default="")
    text = models.CharField(max_length=299)
    date_created = models.DateField(default=str(date.today()))

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Comment class to add comments on a specified note
    """

    text = models.CharField(max_length=299, default="")
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_created = models.DateField(default=str(date.today()))
    date_updated = models.DateField(default=str(date.today()))

    def __str__(self):
        return self.text
