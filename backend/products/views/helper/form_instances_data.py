from products.models import Category, Product, Price
from .get_current_object import get_current_category_obj, get_current_product_object, get_current_seller_obj, \
    get_current_price_obj
from .get_instances_kwargs import get_bsr_category_kwargs, check_kwargs, get_not_bsr_category_kwargs, \
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
    categories_list = objs_querysets['categories_queryset']
    products_list = objs_querysets['product_queryset']
    sellers_list = objs_querysets['sellers_queryset']
    prices_list = objs_querysets['prices_queryset']

    for jobs_data in validated_jobs:
        category_data, category = form_category_data(jobs_data, categories_list)
        categories_bulk_update_list += category_data['categories_bulk_update_list']
        categories_update_fields_list += category_data['categories_update_fields_list']

        product_data, product = form_product_data(jobs_data, category, products_list)
        product_update_list += product_data['product_bulk_update_list']
        product_create_list += product_data['product_bulk_create_list']
        product_update_fields_list += product_data['product_bulk_update_fields_list']

        seller_data = form_seller_and_price_data(jobs_data, product, sellers_list, prices_list)
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
        category_data, category = form_bsr_category_data(product_data, categories_list)
    else:
        category_data, category = form_not_bsr_category_data(product_data, categories_list)

    category_data = {
        'categories_bulk_update_list': category_data['categories_bulk_update_list'],
        'categories_update_fields_list': category_data['categories_update_fields_list'],
    }
    return category_data, category


def form_bsr_category_data(product_data, categories_list):
    categories_bulk_update_list = []
    categories_update_fields_list = []
    category = None
    parent = None
    for category_data in product_data['bsr']:
        category = get_current_category_obj(categories_list, category_data, parent=parent)
        kwargs = get_bsr_category_kwargs(category_data, parent)
        category, categories_bulk_update_list = form_instance_data(Category, category, categories_bulk_update_list,
                                                                   kwargs, save=True)
        categories_update_fields_list = check_kwargs(categories_update_fields_list, kwargs)
        parent = category

    category_data = {
        'categories_bulk_update_list': categories_bulk_update_list,
        'categories_update_fields_list': categories_update_fields_list,
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
