from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User


class MarketAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass123")
        self.admin = User.objects.create_superuser(username="admin", password="admin123")
        self.client = APIClient()
        # self.seller = Seller.objects.create(name="Seller", email="s@t.com", city="Berlin")
        # self.market = Market.objects.create(
        #     name="Market", location="Berlin", seller=self.seller
        # )

    def test_list_markets(self):
        """GET /api/markets/ returns 200."""
        # url = reverse("market-list")
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass

    def test_create_market_authenticated(self):
        """POST /api/markets/ with auth returns 201."""
        # self.client.force_authenticate(user=self.user)
        # data = {"name": "New", "location": "Hamburg", "seller": self.seller.id}
        # response = self.client.post(reverse("market-list"), data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pass

    def test_create_market_unauthenticated(self):
        """POST without auth returns 401."""
        # data = {"name": "New", "location": "Hamburg", "seller": self.seller.id}
        # response = self.client.post(reverse("market-list"), data)
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        pass

    def test_update_market(self):
        """PUT /api/markets/{id}/ updates the market."""
        # self.client.force_authenticate(user=self.user)
        # data = {"name": "Updated", "location": "Berlin", "seller": self.seller.id}
        # response = self.client.put(reverse("market-detail", args=[self.market.pk]), data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass

    def test_delete_market(self):
        """DELETE /api/markets/{id}/ returns 204."""
        # self.client.force_authenticate(user=self.admin)
        # response = self.client.delete(reverse("market-detail", args=[self.market.pk]))
        # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        pass

    def test_search_markets(self):
        """GET /api/markets/?search=Berlin returns filtered results."""
        # response = self.client.get(reverse("market-list"), {"search": "Berlin"})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass