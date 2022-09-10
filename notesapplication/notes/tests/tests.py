import email

import requests
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from user.tests.tests import AuthenticatedTestCase

from .factory import NoteFactory


User = get_user_model()


class CreateNotesAPITestCase(APITestCase):
    url = "/notes/"

    def setUp(self):

        self.user = User.objects.create_user(
            username="nomanbeg",
            password="nomanbeg123",
            email="nomanbeg@hmail.com",
            first_name="noman",
            last_name="beg",
        )

        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        self.token = token.access_token
        self.client.force_login(self.user)
        super().setUp()

        self.note1 = NoteFactory.create(user=self.user)
        self.note2 = NoteFactory.create(user=self.user)

    def test_create_note(self):
        data = {"title": "check search", "text": "search check", "archive": 0}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 201)
        # check title
        self.assertEqual(response.data["title"], "check search")
        # check text
        self.assertEqual(response.data["text"], "search check")

    # check if title is sent blank
    def test_create_note_with_empty_field(self):
        data = {"title": "", "text": "search check", "archive": 0}
        response = self.client.post(self.url, data=data, format="json")
        # status code check
        self.assertEqual(response.status_code, 400)
        # return message check
        self.assertEqual(response.data["title"][0], "This field may not be blank.")

    # check listing of notes
    def test_list_note(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], self.note1.title)
        self.assertEqual(response.data[0]["text"], self.note1.text)

    # check retrieval of note
    def test_retrieve_note(self):
        url = "/notes/1/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.note1.title)
        self.assertEqual(response.data["text"], self.note1.text)

    # check if particular do not exists
    def test_retrieve_note_not_exists(self):
        url = "/notes/3/"
        response = self.client.get(url, format="json")
        # statuscode check
        self.assertEqual(response.status_code, 404)
        # return message check
        self.assertEqual(response.data["detail"], "Not found.")

    # check delete note
    def test_delete_note(self):
        url = "/notes/1/"
        response = self.client.delete(url, format="json")
        # statuscode check
        self.assertEqual(response.status_code, 204)

    # check delete note without passing id
    def test_delete_note_without_id(self):
        response = self.client.delete(self.url, format="json")
        # statuscode check
        self.assertEqual(response.status_code, 405)
        # return message check
        self.assertEqual(response.data["detail"], 'Method "DELETE" not allowed.')
