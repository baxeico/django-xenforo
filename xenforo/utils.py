from django.conf import settings
from django.utils.http import urlencode

def get_avatar_url(username):
    return '%s?%s' % (settings.XENFORO['avatar_api_url'], urlencode({ 'username': username }))
