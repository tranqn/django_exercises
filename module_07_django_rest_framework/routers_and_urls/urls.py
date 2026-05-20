from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import MarketViewSet, SellerViewSet

router = DefaultRouter()
router.register(r"markets", MarketViewSet)
router.register(r"sellers", SellerViewSet)

# Auto-generated URLs:
# GET/POST   /api/markets/
# GET/PUT/DELETE /api/markets/{id}/
# GET        /api/markets/{id}/seller_info/
# GET        /api/markets/recent/
# GET/POST   /api/sellers/
# GET/PUT/DELETE /api/sellers/{id}/

urlpatterns = [
    path("api/", include(router.urls)),
]