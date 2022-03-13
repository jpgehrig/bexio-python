from . import config

# global API configuration
config.api_token = None
config.api_host = 'https://api.bexio.com'

# exceptions
from .api import exceptions  # noqa
