from rest_framework.decorators import action
from rest_framework.response import Response
from .cart import Cart
from products.models import Product
from .serializers import CartItemSerializer
from .viewsets import CartViewSet


class CartView(CartViewSet):
    serializer_class = CartItemSerializer
    cart_manager = Cart
    product_model = Product
    product_lookup_field = 'id'
    queryset = Product.objects.all()

    def checkout(self, request, *args, **kwargs):
        pass
