from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import CartView

app_name = 'rest_framework_cart'

router = DefaultRouter()
router.register(r'', CartView, basename='rest_framework_cart')

urlpatterns = router.urls
