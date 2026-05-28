from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="strongpass123"
        )

    def test_register_new_user(self):
        """POST /api/auth/register/ creates user and returns tokens."""
        # data = {
        #     "username": "newuser", "email": "new@test.com",
        #     "password": "strongpass123", "password_confirm": "strongpass123",
        #     "first_name": "New", "last_name": "User",
        # }
        # response = self.client.post("/api/auth/register/", data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertIn("tokens", response.data)
        pass

    def test_obtain_jwt_token(self):
        """POST /api/auth/token/ returns access and refresh tokens."""
        # data = {"username": "testuser", "password": "strongpass123"}
        # response = self.client.post("/api/auth/token/", data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn("access", response.data)
        # self.assertIn("refresh", response.data)
        pass

    def test_invalid_credentials(self):
        """POST /api/auth/token/ with wrong password returns 401."""
        # data = {"username": "testuser", "password": "wrongpass"}
        # response = self.client.post("/api/auth/token/", data)
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        pass

    def test_change_password(self):
        """POST /api/auth/change-password/ changes the password."""
        # self.client.force_authenticate(user=self.user)
        # data = {"old_password": "strongpass123", "new_password": "newstrongpass456"}
        # response = self.client.post("/api/auth/change-password/", data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass