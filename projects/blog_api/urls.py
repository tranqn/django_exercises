"""URL routing for the blog API."""
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CategoryViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = router.urls

# Project urls.py:
#   path("api/", include("projects.blog_api.urls")),