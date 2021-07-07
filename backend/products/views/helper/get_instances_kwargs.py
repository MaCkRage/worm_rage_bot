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
