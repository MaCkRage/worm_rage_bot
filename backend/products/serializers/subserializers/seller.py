from rest_framework import serializers


class SellerSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    id = serializers.CharField(required=False)
