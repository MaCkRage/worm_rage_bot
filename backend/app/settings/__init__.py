import contextlib

with contextlib.suppress(ImportError):
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())  # load environment variables from .env when using pycharm

from .apps import *
from .base import *
from .languages import *
from .database import *
from .path import *
