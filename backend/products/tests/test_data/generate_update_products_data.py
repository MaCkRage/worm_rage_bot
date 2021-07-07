import random

from utils.utils import get_random_string

categories_list = [
    "Industrial & Scientific",
    "Industrial Labeling Tape",
    "Office Labeling Tapes",
    "Books",
    "Physics",
    "Health & Personal Care",
]

bsr_list = [
    [
        "Industrial & Scientific",
        "Industrial Labeling Tape",
        "Office Labeling Tapes",
    ],
    [
        "Books",
        "Physics",
    ],
    [
        "Health & Personal Care",
    ],
]


def generate_update_products_data(product_count=10, sellers_count=10):
    return {
        "jobs": generate_products_list(product_count, sellers_count)
    }


def generate_products_list(product_count, sellers_count):
    products_list = []
    for i in range(1, product_count + 1):
        product = {
            "image": f"'https://images_{i}'",
            "category": random.choice(categories_list),
            "seller_list": generate_sellers(sellers_count),
            "reviews": {
                "rating_average": random.randint(100, 500) / 100,
                "rating_count": random.randint(1, 1000)
            },
            "id": i,
            "product_link": f"https://www.amazon.com/dp/{i}",
        }
        if i % 3 == 0:
            product["bsr"] = generate_bsr()
        if i % 2 == 0:
            product["date_first_available"] = "2012-08-31"
        products_list.append(product)
    return products_list


def generate_sellers(sellers_count):
    sellers_list = []
    for i in range(1, sellers_count):
        seller_data = {
            "name": get_random_string(10),
            "price": random.randint(1000, 9999) / 100,
        }
        if i % 2 == 0:
            seller_data["id"] = get_random_string(15)
        sellers_list.append(seller_data)
    return sellers_list


def generate_bsr():
    bsr = random.choice(bsr_list)
    bsr_data_list = []
    for category in bsr:
        bsr_data = {
            "position": random.randint(1, 100000),
            "category": category
        }
        bsr_data_list.append(bsr_data)
    return bsr_data_list
