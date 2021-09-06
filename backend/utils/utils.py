"""
python manage.py shell -c "from utils.utils import clear_database; clear_database()"
"""
import time
import random
import string


def get_random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def clear_database():
    pass


start_time = time.time()
end_time = time.time()
dif_time = end_time - start_time
