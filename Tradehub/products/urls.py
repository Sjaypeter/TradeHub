from rest_framework.routers import DefaultRouter
from .views import Productviewset, CategoryViewSet

router = DefaultRouter()
router.register("products", Productviewset, basename="product")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = router.urls