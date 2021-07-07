import json

from django.db import transaction, connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products import serializers
from products.models import Product, Category, Price
from products.views.helper import form_objs_querysets, form_data
from user.models import Seller


@api_view(['POST'])
def update_values_view(request):
    validated_data = serializers.UpdateProductSerializer(data=request.data)
    if validated_data.is_valid():
        validated_dict = json.loads(json.dumps(validated_data.data))
        validated_jobs = validated_dict['jobs']
        update_values(validated_jobs)

        print(len(connection.queries))
        response_status = status.HTTP_201_CREATED
        return Response(status=response_status)
    else:
        response_status = status.HTTP_400_BAD_REQUEST
        errors = validated_data.errors
        return Response(status=response_status, data=errors)


def update_values(validated_jobs):
    objs_querysets = form_objs_querysets(validated_jobs)
    objs_for_update = form_data(validated_jobs, objs_querysets)
    if objs_for_update['categories_bulk_update_list']:
        Category.objects.bulk_update(objs_for_update['categories_bulk_update_list'],
                                     objs_for_update['categories_update_fields_list'])
    if objs_for_update['categories_bulk_create_list']:
        Category.objects.bulk_create(objs_for_update['categories_bulk_create_list'])

    if objs_for_update['product_update_list']:
        Product.objects.bulk_update(objs_for_update['product_update_list'],
                                    objs_for_update['product_update_fields_list'])
    if objs_for_update['product_create_list']:
        Product.objects.bulk_create(objs_for_update['product_create_list'])

    if objs_for_update['sellers_bulk_update_list']:
        Seller.objects.bulk_update(objs_for_update['sellers_bulk_update_list'],
                                   objs_for_update['sellers_update_fields_list'])
    if objs_for_update['sellers_bulk_create_list']:
        Seller.objects.bulk_create(objs_for_update['sellers_bulk_create_list'])

    if objs_for_update['prices_bulk_update_list']:
        Price.objects.bulk_update(objs_for_update['prices_bulk_update_list'],
                                  objs_for_update['prices_update_fields_list'])
    if objs_for_update['prices_bulk_create_list']:
        Price.objects.bulk_create(objs_for_update['prices_bulk_create_list'])

    return
