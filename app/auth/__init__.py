from .common import *
from .local import *

from .facebook import oauth2 as facebook
from .google import oauth2 as google

def get_oauth2_provider(provider: str):
    if provider == 'facebook':
        return facebook
    elif provider == 'google':
        return google
