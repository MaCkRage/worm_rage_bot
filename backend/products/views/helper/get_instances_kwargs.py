def get_bsr_category_kwargs(category_data, parent, category):
    kwargs = {
        'title': category_data['category'],
        'parent': parent,
    }
    if category:
        kwargs['id'] = category['id']
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


def get_not_bsr_category_kwargs(product_data, category):
    kwargs = {
        'title': product_data['category'],
    }
    if category:
        kwargs['id'] = category['id']
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


def set_kwargs(update_fields_list, kwargs):
    for key in list(kwargs.keys()):
        update_fields_list.append(key)
    return update_fields_list
