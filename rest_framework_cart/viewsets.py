from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_cart.cart import Cart
from rest_framework_cart.serializers import CartItemSerializer, CartTotalSerializer


class CartViewSet(GenericViewSet):
    serializer_class = CartItemSerializer
    cart_manager = Cart
    product_model = None
    lookup_field = 'id'
    queryset = None

    def get_cart_manager(self):
        assert self.cart_manager is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.__manager

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def __initialize_cart(self, request):
        self.__manager = self.cart_manager(request, self.product_model, self.lookup_field)
        return self.__manager

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        self.__initialize_cart(request)
        return request

    @action(methods=['PUT'], detail=True)
    def change(self, request,  *args,  **kwargs):
        obj = self.get_object()
        cart = self.get_cart_manager()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cart.change(obj, serializer.validated_data['quantity'], serializer.validated_data['update'])
        queryset = cart.items
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['DELETE'], detail=False)
    def clean(self, request, *args, **kwargs):
        cart = self.get_cart_manager()
        cart.clear()
        return Response(status=200)

    def list(self, request, *args, **kwargs):
        cart = self.get_cart_manager()
        page = self.paginate_queryset(cart.items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(cart.items, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, serializer_class=CartTotalSerializer)
    def total(self, request, *args, **kwargs):
        cart = self.get_cart_manager()
        return Response(self.get_serializer({'total': cart.total,
                                             'size': cart.size}).data)
