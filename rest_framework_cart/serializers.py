from rest_framework import serializers


class CartItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(read_only=True)
    price = serializers.FloatField(read_only=True)
    quantity = serializers.IntegerField(required=True)
    update = serializers.BooleanField(write_only=True, default=False)
    subtotal = serializers.FloatField(read_only=True)


class CartTotalSerializer(serializers.Serializer):
    total = serializers.FloatField(read_only=True)
    size = serializers.IntegerField(read_only=True)
