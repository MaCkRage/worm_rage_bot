import json

from django.db import transaction, connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products import serializers

from django.db import connection


@api_view(['POST'])
def update_values_view(request):
    validated_data = serializers.UpdateProductSerializer(data=request.data)
    if validated_data.is_valid():
        validated_dict = json.loads(json.dumps(validated_data.data))
        validated_jobs = validated_dict['jobs']
        update_values(validated_jobs)

        # print(len(connection.queries))
        response_status = status.HTTP_201_CREATED
        return Response(status=response_status)
    else:
        response_status = status.HTTP_400_BAD_REQUEST
        errors = validated_data.errors
        return Response(status=response_status, data=errors)


@transaction.atomic
def update_values(validated_jobs):
    objs_querysets = form_objs_lists(validated_jobs)
    objs_for_update = form_data(validated_jobs, objs_querysets)
    if objs_for_update['categories_bulk_update_list']:
        Category.objects.bulk_update(objs_for_update['categories_bulk_update_list'],
                                     objs_for_update['categories_update_fields_list'])
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


def form_data(validated_jobs, objs_querysets):
    product_update_list = []
    product_create_list = []
    product_update_fields_list = []
    categories_bulk_create_list = []
    categories_bulk_update_list = []
    categories_update_fields_list = []
    sellers_bulk_create_list = []
    sellers_bulk_update_list = []
    sellers_update_fields_list = []
    prices_bulk_create_list = []
    prices_bulk_update_list = []
    prices_update_fields_list = []
    categories_list = objs_querysets['categories_queryset']
    products_list = objs_querysets['product_queryset']
    sellers_list = objs_querysets['sellers_queryset']
    prices_list = objs_querysets['prices_queryset']

    for jobs_data in validated_jobs:
        print(print(len(connection.queries)))
        category_data, category = form_category_data(jobs_data, categories_list)
        categories_bulk_update_list += category_data['categories_bulk_update_list']
        categories_update_fields_list += category_data['categories_update_fields_list']
        if category_data.get('parent_categories_list'):
            categories_list += category_data['parent_categories_list']
        print(len(connection.queries))
        product_data, product = form_product_data(jobs_data, category, products_list)
        product_update_list += product_data['product_bulk_update_list']
        product_create_list += product_data['product_bulk_create_list']
        product_update_fields_list += product_data['product_bulk_update_fields_list']
        print(len(connection.queries))
        seller_data = form_seller_and_price_data(jobs_data, product, sellers_list, prices_list)
        sellers_bulk_create_list += seller_data['sellers_bulk_create_list']
        sellers_bulk_update_list += seller_data['sellers_bulk_update_list']
        sellers_update_fields_list += seller_data['sellers_update_fields_list']
        print(len(connection.queries))
        prices_bulk_create_list += seller_data['prices_bulk_create_list']
        prices_bulk_update_list += seller_data['prices_bulk_update_list']
        prices_update_fields_list += seller_data['prices_update_fields_list']

    product_update_fields_list = list(set(product_update_fields_list))
    categories_update_fields_list = list(set(categories_update_fields_list))
    sellers_update_fields_list = list(set(sellers_update_fields_list))
    prices_update_fields_list = list(set(prices_update_fields_list))

    if 'id' in product_update_fields_list:
        product_update_fields_list.remove('id')

    formed_data = {
        'product_update_list': product_update_list,
        'product_create_list': product_create_list,
        'product_update_fields_list': product_update_fields_list,
        'categories_bulk_create_list': categories_bulk_create_list,
        'categories_bulk_update_list': categories_bulk_update_list,
        'categories_update_fields_list': categories_update_fields_list,
        'sellers_bulk_create_list': sellers_bulk_create_list,
        'sellers_bulk_update_list': sellers_bulk_update_list,
        'sellers_update_fields_list': sellers_update_fields_list,
        'prices_bulk_create_list': prices_bulk_create_list,
        'prices_bulk_update_list': prices_bulk_update_list,
        'prices_update_fields_list': prices_update_fields_list,
    }
    return formed_data


def form_category_data(product_data, categories_list):
    if product_data.get('bsr'):
        category_objs_data, category = form_bsr_category_data(product_data, categories_list)
    else:
        category_objs_data, category = form_not_bsr_category_data(product_data, categories_list)

    category_data = {
        'categories_bulk_update_list': category_objs_data['categories_bulk_update_list'],
        'categories_update_fields_list': category_objs_data['categories_update_fields_list'],
    }
    if category_data.get('parent_categories_list'):
        category_data['parent_categories_list'] = category_objs_data['parent_categories_list']
    return category_data, category


def form_bsr_category_data(product_data, categories_list):
    categories_bulk_update_list = []
    categories_update_fields_list = []
    parent_categories_list = []
    category = None
    parent = None
    for category_data in product_data['bsr']:
        category = get_current_category_obj(categories_list, category_data, parent=parent)
        kwargs = get_bsr_category_kwargs(category_data, parent)
        category, categories_bulk_update_list = form_instance_data(Category, category, categories_bulk_update_list,
                                                                   kwargs, save=True)
        categories_update_fields_list = check_kwargs(categories_update_fields_list, kwargs)
        parent_categories_list.append(parent)
        parent = category

    category_data = {
        'categories_bulk_update_list': categories_bulk_update_list,
        'categories_update_fields_list': categories_update_fields_list,
        'parent_categories_list': parent_categories_list
    }
    return category_data, category


def form_not_bsr_category_data(product_data, categories_list):
    categories_bulk_update_list = []
    categories_update_fields_list = []
    kwargs = get_not_bsr_category_kwargs(product_data)
    category = get_current_category_obj(categories_list, product_data)
    category, categories_bulk_update_list = form_instance_data(Category, category, categories_bulk_update_list,
                                                               kwargs, save=True)
    categories_update_fields_list = check_kwargs(categories_update_fields_list, kwargs)
    category_data = {
        'categories_bulk_update_list': categories_bulk_update_list,
        'categories_update_fields_list': categories_update_fields_list,
    }
    return category_data, category


def form_product_data(product_data, category, products_list):
    product_bulk_update_list = []
    product_bulk_create_list = []
    product_bulk_update_fields_list = []
    kwargs = get_product_kwargs(product_data, category)

    product = get_current_product_object(products_list, product_data)
    product, product_bulk_update_list, product_bulk_create_list = form_instance_data(Product, product,
                                                                                     product_bulk_update_list, kwargs,
                                                                                     bulk_create_list=product_bulk_create_list,
                                                                                     pop_field='id')
    product_bulk_update_fields_list = check_kwargs(product_bulk_update_fields_list, kwargs)

    product_data = {
        'product_bulk_update_list': product_bulk_update_list,
        'product_bulk_create_list': product_bulk_create_list,
        'product_bulk_update_fields_list': product_bulk_update_fields_list,
    }
    return product_data, product


def form_seller_and_price_data(product_data, product, sellers_list, prices_list):
    sellers_bulk_create_list = []
    sellers_bulk_update_list = []
    sellers_update_fields_list = []
    prices_bulk_create_list = []
    prices_bulk_update_list = []
    prices_update_fields_list = []
    for seller_price_data in product_data['seller_list']:
        seller_data, seller = form_seller_data(seller_price_data, sellers_list)
        sellers_bulk_update_list += seller_data['sellers_bulk_update_list']
        sellers_bulk_create_list += seller_data['sellers_bulk_create_list']
        sellers_update_fields_list += seller_data['sellers_update_fields_list']

        prices_data = form_prices_data(seller_price_data, product, seller, prices_list)
        prices_bulk_create_list += prices_data['prices_bulk_create_list']
        prices_bulk_update_list += prices_data['prices_bulk_update_list']
        prices_update_fields_list += prices_data['prices_update_fields_list']

    seller_price_data = {
        'sellers_bulk_create_list': sellers_bulk_create_list,
        'sellers_bulk_update_list': sellers_bulk_update_list,
        'sellers_update_fields_list': sellers_update_fields_list,
        'prices_bulk_create_list': prices_bulk_create_list,
        'prices_bulk_update_list': prices_bulk_update_list,
        'prices_update_fields_list': prices_update_fields_list,
    }
    return seller_price_data


def form_seller_data(seller_price_data, sellers_list):
    sellers_bulk_update_list = []
    sellers_bulk_create_list = []
    sellers_update_fields_list = []

    kwargs = get_seller_kwargs(seller_price_data)
    seller = get_current_seller_obj(sellers_list, seller_price_data)
    seller, sellers_bulk_update_list, sellers_bulk_create_list = form_instance_data(Seller, seller,
                                                                                    sellers_bulk_update_list, kwargs,
                                                                                    bulk_create_list=sellers_bulk_create_list)
    sellers_update_fields_list = check_kwargs(sellers_update_fields_list, kwargs)
    seller_data = {
        'sellers_bulk_update_list': sellers_bulk_update_list,
        'sellers_bulk_create_list': sellers_bulk_create_list,
        'sellers_update_fields_list': sellers_update_fields_list,
    }
    return seller_data, seller


def form_prices_data(seller_data, product, seller, prices_list):
    prices_bulk_create_list = []
    prices_bulk_update_list = []
    prices_update_fields_list = []

    kwargs = get_prices_kwargs(seller_data, seller, product)
    price = get_current_price_obj(prices_list, seller, product)
    instance, prices_bulk_update_list, prices_bulk_create_list = form_instance_data(Price, price,
                                                                                    prices_bulk_update_list, kwargs,
                                                                                    bulk_create_list=prices_bulk_create_list)
    prices_update_fields_list = check_kwargs(prices_update_fields_list, kwargs)

    prices_data = {
        'prices_bulk_create_list': prices_bulk_create_list,
        'prices_bulk_update_list': prices_bulk_update_list,
        'prices_update_fields_list': prices_update_fields_list,
    }
    return prices_data


def form_instance_data(model, instance, bulk_update_list, kwargs_data, **kwargs):
    if instance:
        pop_field = kwargs.get('pop_field')
        if pop_field is not None:
            kwargs_data.pop(pop_field)
        instance.update_fields(kwargs_data)
        bulk_update_list.append(instance)

    else:
        instance = model(**kwargs_data)
        if kwargs.get('save'):
            instance.save()

        bulk_create_list = kwargs.get('bulk_create_list')
        if bulk_create_list is not None:
            bulk_create_list.append(instance)
            return instance, bulk_update_list, bulk_create_list

    bulk_create_list = kwargs.get('bulk_create_list')
    if bulk_create_list is not None:
        return instance, bulk_update_list, kwargs.get('bulk_create_list'),
    return instance, bulk_update_list


from products.models import Category, Product, Price
from user.models import Seller


def form_objs_lists(validated_jobs):
    objects_values_lists = form_objs_values_lists(validated_jobs)
    categories_queryset = Category.objects.filter(
        title__in=objects_values_lists['categories_titles_list']).prefetch_related('product_category')
    products_queryset = Product.objects.filter(id__in=objects_values_lists['products_id_list']).prefetch_related(
        'product_prices')
    prices_queryset = Price.objects.filter(
        seller__title__in=objects_values_lists['sellers_titles_list']).select_related('seller').select_related(
        'product')
    sellers_queryset = Seller.objects.filter(title__in=objects_values_lists['sellers_titles_list'])
    formed_data = {
        'categories_queryset': categories_queryset,
        'product_queryset': products_queryset,
        'prices_queryset': prices_queryset,
        'sellers_queryset': sellers_queryset,
    }
    return formed_data


def form_objs_values_lists(validated_jobs):
    products_id_list = []
    categories_titles_list = []
    sellers_titles_list = []
    for jobs_data in validated_jobs:
        products_id_list = form_values_list(products_id_list, value=jobs_data['id'])
        categories_titles_list = form_category_titles_list(jobs_data, categories_titles_list)
        sellers_titles_list = form_sellers_values_list(jobs_data, sellers_titles_list)

    objects_values_lists = {
        'products_id_list': products_id_list,
        'categories_titles_list': categories_titles_list,
        'sellers_titles_list': sellers_titles_list,
    }
    return objects_values_lists


def form_category_titles_list(jobs_data, categories_titles_list):
    if jobs_data.get('bsr'):
        for category_data in jobs_data['bsr']:
            categories_titles_list = form_values_list(categories_titles_list, value=category_data['category'])
            return categories_titles_list
    categories_titles_list = form_values_list(categories_titles_list, value=jobs_data['category'])
    return categories_titles_list


def form_sellers_values_list(jobs_data, sellers_names_list):
    for seller_data in jobs_data['seller_list']:
        sellers_names_list = form_values_list(sellers_names_list, value=seller_data['name'])
    return sellers_names_list


def form_values_list(objs_values_list, value):
    if value not in objs_values_list:
        objs_values_list.append(value)
    return objs_values_list


def get_current_category_obj(categories_list, category_data, **kwargs):
    parent = kwargs.get('parent')
    if parent:
        for category in categories_list:
            if category.title == category_data['category'] and category.parent == parent:
                return category
        return None
    for category in categories_list:
        if category.title == category_data['category']:
            return category
    return None


def get_current_product_object(products_list, product_data):
    for product in products_list:
        if product.pk == product_data['id']:
            return product
    return None


def get_current_seller_obj(sellers_list, seller_price_data):
    for seller in sellers_list:
        if seller.title == seller_price_data['name']:
            return seller
    return None


def get_current_price_obj(prices_list, seller, product):
    for price in prices_list:
        if price.seller == seller and price.product == product:
            return price
    return None


def get_bsr_category_kwargs(category_data, parent):
    kwargs = {
        'title': category_data['category'],
        'parent': parent,
    }
    return kwargs


def get_product_kwargs(product_data, category):
    kwargs = {
        'id': product_data['id'],
        'image': product_data['image'],
        'category': category,
        'rating_average': product_data['reviews']['rating_average'],
        'rating_count': product_data['reviews']['rating_count'],
        'product_link': product_data['product_link'],
    }
    if product_data.get('date_first_available'):
        kwargs['date_first_available'] = product_data['date_first_available']
    return kwargs


def get_not_bsr_category_kwargs(product_data):
    kwargs = {
        'title': product_data['category'],
        'lft': 0,
        'rght': 0,
        'level': 0,
        'tree_id': 0,
    }
    return kwargs


def get_seller_kwargs(seller_price_data):
    kwargs = {
        'title': seller_price_data['name'],
    }
    if seller_price_data.get('id'):
        kwargs['seller_id'] = seller_price_data['id']
    return kwargs


def get_prices_kwargs(seller_data, seller, product):
    kwargs = {
        'seller': seller,
        'product': product,
        'price': seller_data.get('price')
    }
    return kwargs


def check_kwargs(update_fields_list, kwargs):
    for key in list(kwargs.keys()):
        if key not in update_fields_list:
            update_fields_list.append(key)
    return update_fields_list
