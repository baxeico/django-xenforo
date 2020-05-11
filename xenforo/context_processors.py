from django.conf import settings

def xenforo_urls(request):
    return {
        'xenforo_login': settings.XENFORO['login_url'],
    }
