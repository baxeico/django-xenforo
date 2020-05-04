from time import time
import logging

from django.conf import settings

from .models import XenforoUser, XenforoSession

logger = logging.getLogger(__name__)

class XFSessionMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if 'xenforo_username' not in request.session:
            xf_session_id = request.COOKIES.get(settings.XENFORO['cookie_prefix'] + 'session', None)

            request.xf_session = None
            if xf_session_id:
                try:
                    xenforosession = XenforoSession.objects.using(settings.XENFORO['database']).get(pk=xf_session_id, expiry_date__gte=int(time()))
                except XenforoSession.DoesNotExist:
                    pass
                else:
                    request.xf_session = xenforosession.get_session_data()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class XFRemoteUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if 'xenforo_username' in request.session:
            request.META['REMOTE_USER'] = request.session['xenforo_username']
        else:
            assert hasattr(request, 'xf_session'), "The XFRemoteUserMiddleware middleware requires the XFSessionMiddleware middleware to be installed."
            try:
                lookup_user_id = int(request.xf_session.get(b'userId'))
            except:
                pass
            else:
                try:
                    xenforouser = XenforoUser.objects.using(settings.XENFORO['database']).get(pk=lookup_user_id)
                except XenforoUser.DoesNotExist:
                    pass
                else:
                    if xenforouser.user_state == 'valid' and xenforouser.is_banned == '0':
                        request.META['REMOTE_USER'] = xenforouser.username
                        request.session['xenforo_username'] = xenforouser.username

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
