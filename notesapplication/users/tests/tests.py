from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from users.tests.factory import UserFactory


class AuthenticatedTestCase(APITestCase):
    """Test Case class for authenticated requests."""

    user = None

    @classmethod
    def create_user_token(cls, user):
        """Create user token and add it in user."""

        refresh = RefreshToken.for_user(user)
        user.refresh_token = str(refresh)
        user.access_token = str(refresh.access_token)

    def setUp(self):
        super().setUp()

        user, token = AuthenticatedTestCase.create_user_token(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {token}")
        self.user = user
        self.token = token
        self.client.force_login(user)


class UserLoginTestCase(APITestCase):
    """Test Class to test user login API."""

    def setUp(self):
        self.url = "/login"
        self.user1 = UserFactory.create()
        self.user1.set_password("!@#123")
        self.user1.save()

    def test_login_api(self):
        self.data = {
            "username": self.user1.username,
            "password": "!@#123",
        }
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, 200)
        response_data = response.data

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_api_with_wrong_credentials(self):
        self.data = {
            "username": "notrandom",
            "password": "!@#123",
        }
        response = self.client.post(self.url, self.data, format="json")

        # Unauthorized user
        self.assertEqual(response.status_code, 401)
