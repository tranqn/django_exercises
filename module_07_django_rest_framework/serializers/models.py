from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="markets")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name