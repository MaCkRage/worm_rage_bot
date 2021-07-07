"""
python manage.py shell -c "from utils.utils import clear_database; clear_database()"
"""
import time

from products.models import Category, Price, Product
from user.models import Seller
import random
import string


def get_random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def clear_database():
    Category.objects.all().delete()
    Price.objects.all().delete()
    Product.objects.all().delete()
    Seller.objects.all().delete()


start_time = time.time()
end_time = time.time()
dif_time = end_time - start_time
