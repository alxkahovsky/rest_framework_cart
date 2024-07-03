# Библиотека для обработки корзины в rest_framework проектах. 
Используется session_backend

## Установка и использование
pip install <package_name>
`INSTALLED_APPS = [
    'rest_framework_cart',
    ...
]`

создаем приложение `cart` коммандой `python startapp cart`,
далее в файле `cart\views`:

`
from rest_framework_cart.cart import Cart
from rest_framework_cart.serializers import CartItemSerializer
from rest_framework_cart.viewsets import CartViewSet

from products.models import Product  # Необходимо использовать модель товара


class CartView(CartViewSet):
    serializer_class = CartItemSerializer
    cart_manager = Cart
    product_model = Product
    product_lookup_field = 'id'
    queryset = Product.objects.all()

    def checkout(self, request, *args, **kwargs):
        pass
`

Далее добавим код в файл `cart/urls`:

`from rest_framework.routers import DefaultRouter
from .views import CartView

app_name = 'cart'

router = DefaultRouter()
router.register(r'', CartView, basename='cart')

urlpatterns = router.urls`
