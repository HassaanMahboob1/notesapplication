# Generated by Django 4.1.1 on 2022-09-07 09:47
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0002_alter_note_date_created_alter_note_text_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="noteversion",
            name="title",
            field=models.CharField(default="", max_length=39),
        ),
    ]
