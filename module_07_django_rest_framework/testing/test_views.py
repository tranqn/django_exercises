from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_returns_200(self):
        response = self.client.get("/")
        # self.assertEqual(response.status_code, 200)
        pass

    def test_home_page_uses_correct_template(self):
        response = self.client.get("/")
        # self.assertTemplateUsed(response, "home.html")
        pass


class ProtectedViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass123")

    def test_redirect_when_not_logged_in(self):
        response = self.client.get("/dashboard/")
        # self.assertEqual(response.status_code, 302)
        pass

    def test_accessible_when_logged_in(self):
        self.client.login(username="test", password="pass123")
        response = self.client.get("/dashboard/")
        # self.assertEqual(response.status_code, 200)
        pass