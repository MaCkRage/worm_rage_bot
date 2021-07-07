from django.db import connection

from products.models import Category, Product, Price
from .get_current_object import get_no_bsr_current_category_obj, is_product, get_current_seller_obj, \
    get_current_price_obj, get_bsr_category_obj
from .get_instances_kwargs import get_bsr_category_kwargs, set_kwargs, get_not_bsr_category_kwargs, \
    get_product_kwargs, get_seller_kwargs, get_prices_kwargs
from user.models import Seller


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
    parents_list = []
    categories_queryset = objs_querysets['categories_queryset']
    products_queryset = objs_querysets['product_queryset']
    sellers_queryset = objs_querysets['sellers_queryset']
    prices_queryset = objs_querysets['prices_queryset']
    for jobs_data in validated_jobs:
        category_data, category = form_category_data(jobs_data, categories_queryset)
        categories_bulk_create_list += category_data['categories_bulk_create_list']
        categories_bulk_update_list += category_data['categories_bulk_update_list']
        categories_update_fields_list += category_data['categories_update_fields_list']
        if category_data.get('parents_list'):
            parents_list += category_data['parents_list']

        product_data, product = form_product_data(jobs_data, category, products_queryset)
        product_update_list += product_data['product_bulk_update_list']
        product_create_list += product_data['product_bulk_create_list']
        product_update_fields_list += product_data['product_bulk_update_fields_list']

        seller_data = form_seller_and_price_data(jobs_data, product, sellers_queryset, prices_queryset)
        sellers_bulk_create_list += seller_data['sellers_bulk_create_list']
        sellers_bulk_update_list += seller_data['sellers_bulk_update_list']
        sellers_update_fields_list += seller_data['sellers_update_fields_list']

        prices_bulk_create_list += seller_data['prices_bulk_create_list']
        prices_bulk_update_list += seller_data['prices_bulk_update_list']
        prices_update_fields_list += seller_data['prices_update_fields_list']
    product_update_fields_list = list(set(product_update_fields_list))
    categories_update_fields_list = list(set(categories_update_fields_list))
    sellers_update_fields_list = list(set(sellers_update_fields_list))
    prices_update_fields_list = list(set(prices_update_fields_list))

    if 'id' in product_update_fields_list:
        product_update_fields_list.remove('id')
    if 'id' in categories_update_fields_list:
        categories_update_fields_list.remove('id')
    if 'id' in sellers_update_fields_list:
        sellers_update_fields_list.remove('id')
    if 'id' in prices_update_fields_list:
        prices_update_fields_list.remove('id')

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


def form_category_data(product_data, categories_queryset):
    if product_data.get('bsr'):
        category_objs_data, category = form_bsr_category_data(product_data, categories_queryset)
    else:
        category_objs_data, category = form_not_bsr_category_data(product_data, categories_queryset)

    category_data = {
        'categories_bulk_update_list': category_objs_data['categories_bulk_update_list'],
        'categories_update_fields_list': category_objs_data['categories_update_fields_list'],
        'categories_bulk_create_list': category_objs_data['categories_bulk_create_list'],
    }
    if category_objs_data.get('parents_list'):
        category_data['parents_list'] = category_objs_data['parents_list']
    return category_data, category


def form_bsr_category_data(product_data, categories_list):
    categories_bulk_update_list = []
    categories_bulk_create_list = []
    categories_update_fields_list = []
    parents_list = []
    category = None
    parent = None
    for category_data in product_data['bsr']:
        category = get_bsr_category_obj(categories_list, category_data, parent=parent)
        kwargs = get_bsr_category_kwargs(category_data, parent, category)
        category, categories_bulk_update_list, categories_bulk_create_list = form_bsr_object_category_data(categories_bulk_update_list, categories_bulk_create_list, kwargs, category)
        categories_update_fields_list = set_kwargs(categories_update_fields_list, kwargs)
        parents_list.append(parent)
        parent = category
    category_data = {
        'categories_bulk_update_list': categories_bulk_update_list,
        'categories_bulk_create_list': categories_bulk_create_list,
        'categories_update_fields_list': categories_update_fields_list,
        'parents_list': parents_list
    }
    return category_data, category


def form_not_bsr_category_data(product_data, categories_list):
    categories_bulk_update_list = []
    categories_update_fields_list = []
    categories_bulk_create_list = []
    category = get_no_bsr_current_category_obj(categories_list, product_data)
    kwargs = get_not_bsr_category_kwargs(product_data, category)
    category, categories_bulk_update_list, categories_bulk_create_list = form_no_bsr_object_category_data(categories_bulk_update_list, categories_bulk_create_list, kwargs, )
    categories_update_fields_list = set_kwargs(categories_update_fields_list, kwargs)
    category_data = {
        'categories_bulk_update_list': categories_bulk_update_list,
        'categories_bulk_create_list': categories_bulk_create_list,
        'categories_update_fields_list': categories_update_fields_list,
    }
    return category_data, category


def form_product_data(product_data, category, products_list):
    product_bulk_update_fields_list = []
    product = is_product(products_list, product_data)
    kwargs = get_product_kwargs(product_data, category)
    product_obj, product_bulk_create_list, product_bulk_update_list = form_object_product_data(kwargs, product)
    product_bulk_update_fields_list = set_kwargs(product_bulk_update_fields_list, kwargs)

    product_data = {
        'product_bulk_update_list': product_bulk_update_list,
        'product_bulk_create_list': product_bulk_create_list,
        'product_bulk_update_fields_list': product_bulk_update_fields_list,
    }
    return product_data, product_obj


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

    # kwargs = get_seller_kwargs(seller_price_data)
    seller = get_current_seller_obj(sellers_list, seller_price_data)
    # seller, sellers_bulk_update_list, sellers_bulk_create_list = form_instance_data(Seller,
    #                                                                                 sellers_bulk_update_list, kwargs,
    #                                                                                 bulk_create_list=sellers_bulk_create_list)
    # sellers_update_fields_list = check_kwargs(sellers_update_fields_list, kwargs)
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

    # kwargs = get_prices_kwargs(seller_data, seller, product)
    # price = get_current_price_obj(prices_list, seller, product)
    # instance, prices_bulk_update_list, prices_bulk_create_list = form_instance_data(Price,
    #                                                                                 prices_bulk_update_list, kwargs,
    #                                                                                 bulk_create_list=prices_bulk_create_list)
    # prices_update_fields_list = check_kwargs(prices_update_fields_list, kwargs)

    prices_data = {
        'prices_bulk_create_list': prices_bulk_create_list,
        'prices_bulk_update_list': prices_bulk_update_list,
        'prices_update_fields_list': prices_update_fields_list,
    }
    return prices_data


# def form_instance_data(model, bulk_update_list, kwargs_data, **kwargs):
#     if kwargs_data.get('id'):
#         pop_field = kwargs.get('pop_field')
#         if pop_field is not None:
#             kwargs_data.pop(pop_field)
#         instance = model(**kwargs_data)
#         bulk_update_list.append(instance)
#
#     else:
#         instance = model(**kwargs_data)
#         if kwargs.get('save'):
#             instance.save()
#
#         bulk_create_list = kwargs.get('bulk_create_list')
#         if bulk_create_list is not None:
#             bulk_create_list.append(instance)
#             return instance, bulk_update_list, bulk_create_list
#
#     bulk_create_list = kwargs.get('bulk_create_list')
#     if bulk_create_list is not None:
#         return instance, bulk_update_list, kwargs.get('bulk_create_list'),
#     return instance, bulk_update_list

def form_no_bsr_object_category_data(categories_bulk_update_list, categories_bulk_create_list, kwargs_data):
    if kwargs_data.get('id'):
        category_obj = Category(**kwargs_data)
        categories_bulk_update_list.append(category_obj)
    category_obj = Category(**kwargs_data)
    categories_bulk_create_list.append(category_obj)
    return category_obj, categories_bulk_update_list, categories_bulk_create_list


def form_bsr_object_category_data(categories_bulk_update_list, categories_bulk_create_list, kwargs_data, category):
    if category:
        category_obj = Category(**kwargs_data)
        categories_bulk_update_list.append(category_obj)
    category_obj = Category(**kwargs_data)
    categories_bulk_create_list.append(category_obj)
    return category_obj, categories_bulk_update_list, categories_bulk_create_list


def form_object_product_data(kwargs_data, product):
    product_bulk_update_list = []
    product_bulk_create_list = []
    if product:
        product_obj = Product(**kwargs_data)
        product_bulk_update_list.append(product_obj)
        return product_obj, product_bulk_create_list, product_bulk_update_list
    product_obj = Product(**kwargs_data)
    product_bulk_create_list.append(product_obj)
    return product_obj, product_bulk_create_list, product_bulk_update_list
