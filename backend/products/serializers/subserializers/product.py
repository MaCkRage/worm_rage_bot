from rest_framework import serializers

from .seller import SellerSerializer
from .review import ReviewSerializer
from .bsr import BsrSerializer

class ProductSerializer(serializers.Serializer):
    image = serializers.CharField(required=True)
    category = serializers.CharField(required=True)
    seller_list = serializers.ListField(child=SellerSerializer(required=True))
    bsr = serializers.ListField(child=BsrSerializer(required=False), required=False)
    reviews = ReviewSerializer(required=True)
    date_first_available = serializers.DateTimeField(input_formats=["%Y-%M-%d"], required=False)
    id = serializers.IntegerField()
    product_link = serializers.CharField()

