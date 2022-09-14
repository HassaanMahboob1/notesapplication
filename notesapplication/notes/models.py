from datetime import date

from django.db import models
from user.models import Users


class Note(models.Model):
    """
    Note class to perform CRUD operations on Note
    """

    title = models.CharField(max_length=31, default="")
    text = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)
    sharedwith = models.ManyToManyField(Users, related_name="sharedwith", blank=True)

    def __str__(self):
        return self.text


class NoteVersion(models.Model):
    """
    NoteVersion class to add versions of a note
    """

    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    edited_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=31, default="")
    text = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Comment class to add comments on a specified note
    """

    text = models.CharField(max_length=255, default="")
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
