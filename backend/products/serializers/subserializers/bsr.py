from rest_framework import serializers


class BsrSerializer(serializers.Serializer):
    position = serializers.IntegerField(required=True)
    category = serializers.CharField(required=True)