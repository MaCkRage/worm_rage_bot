def get_bsr_category_obj(categories_list, category_data, parent):
    if categories_list:
        for category in categories_list:
            if category['title'] == category_data['category'] and category['parent'] == parent:
                return category
    return None


def get_no_bsr_current_category_obj(categories_list, category_data):
    if categories_list:
        for category in categories_list:
            if category['title'] == category_data['category']:
                return category
    return None


def is_product(products_list, product_data):
    if products_list:
        for product in products_list:
            if product['id'] == product_data['id']:
                return True
    return False


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
