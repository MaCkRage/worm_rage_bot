from rest_framework import serializers


class ReviewSerializer(serializers.Serializer):
    rating_average = serializers.DecimalField(required=True, max_digits=10,  decimal_places=2)
    rating_count = serializers.IntegerField()