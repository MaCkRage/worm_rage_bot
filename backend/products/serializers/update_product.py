from rest_framework import serializers
from products.serializers import subserializers

class UpdateProductSerializer(serializers.Serializer):
    jobs = serializers.ListField(child=subserializers.ProductSerializer(required=True))