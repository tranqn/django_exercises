from django.urls import path
from . import function_views

urlpatterns = [
    path("markets/", function_views.market_list, name="market-list"),
    path("markets/<int:pk>/", function_views.market_detail, name="market-detail"),
]