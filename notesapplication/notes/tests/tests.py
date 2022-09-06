from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import requests


class TestViewSets(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self._url = "http://127.0.0.1:8000/"
        self.token = ""

    def test_register_POST(self):
        register = self._url + "register"
        client = Client()
        data = {
            "email": "usmano.beg@gmail.com",
            "first_name": "usmano",
            "last_name": "beg",
            "username": "usmanobeg",
            "password": "usmanobeg123",
        }
        response = client.post(register, data=data, format="json")
        self.assertEquals(response.status_code, 201)

    def test_Login_POST(self):
        self.test_register_POST()
        login = self._url + "api/token/"
        data = {"username": "usmanobeg", "password": "usmanobeg123"}
        response = self.client.post(login, data=data, format="json")
        data = response.json()
        self.token = data["access"]
        self.assertEquals(response.status_code, 200)

    def test_create_note_POST(self):
        self.test_Login_POST()
        create_note = self._url + "Notes/"
        hed = {"Authorization": "Bearer " + self.token}
        data = {
            "title": "Note 6",
            "text": "sixth-Party",
            "date_created": "2022-08-30",
            "date_updated": "2022-08-30",
            "archive": 0,
        }
        response = requests.post(create_note, data=data, headers=hed)
        self.assertEquals(response.status_code, 201)

    def test_notes_list_GET(self):
        self.test_Login_POST()
        create_note = self._url + "Notes/"
        hed = {"Authorization": "Bearer " + self.token}
        response = requests.get(create_note, headers=hed)
        self.assertEquals(response.status_code, 200)

    def test_notes_delete_DELETE(self):
        self.test_Login_POST()
        create_note = self._url + "Notes/30/"
        hed = {"Authorization": "Bearer " + self.token}
        response = requests.delete(create_note, headers=hed)
        self.assertEquals(response.status_code, 204)
