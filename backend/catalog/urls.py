from rest_framework.routers import DefaultRouter
from .views import BaseItemViewSet, UniqueItemViewSet

router = DefaultRouter()
router.register(r"base-items", BaseItemViewSet, basename="base-item")
router.register(r"uniques", UniqueItemViewSet, basename="unique-item")

urlpatterns = router.urls