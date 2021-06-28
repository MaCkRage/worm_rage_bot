import os
from .path import BASE_DIR

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGE_CODE = 'ru'

USE_DEFAULT_LANGUAGE_PREFIX = False

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# DATE_FORMAT = '%m/%d/%y'
# SHORT_DATE_FORMAT = '%m/%d/%y'
#
# DATE_INPUT_FORMATS = [
#     '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
#     '%Y.%m.%d', '%m.%d.%Y', '%m.%d.%y',
#     '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
#     '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
#     '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
#     '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
# ]

DATE_INPUT_FORMATS = ['%d.%m.%Y', '%d-%m-%Y']
SHORT_DATE_FORMAT = '%d.%m.%Y'
DATE_FORMAT = '%d.%m.%Y'