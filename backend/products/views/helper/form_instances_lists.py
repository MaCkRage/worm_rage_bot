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
        'categories_queryset': list(categories_queryset),
        'product_queryset': list(products_queryset),
        'prices_queryset': list(prices_queryset),
        'sellers_queryset': list(sellers_queryset),
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
