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
