from time import time
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib import auth

from .models import XenforoUser, XenforoSession

logger = logging.getLogger(__name__)

class XFSessionMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if 'xf_user_id' not in request.session:
            xf_session_id = request.COOKIES.get(settings.XENFORO['cookie_prefix'] + 'session', None)
            if xf_session_id:
                try:
                    xenforosession = XenforoSession.objects.using(settings.XENFORO['database']).get(pk=xf_session_id, expiry_date__gte=int(time()))
                except XenforoSession.DoesNotExist:
                    pass
                else:
                    php_session_data = xenforosession.get_session_data()
                    try:
                        request.session['xf_user_id'] = int(php_session_data.get(b'userId'))
                    except:
                        # not found a valid Xenforo userID in session data. No login!
                        pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class XFUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The XFUserMiddleware auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the XFUserMiddleware class.")
        if request.user.is_authenticated:
            return self.get_response(request)

        # user is not logged in, search for Xenforo session data to get the Xenforo userId in current session
        if 'xf_user_id' in request.session:
            # found a Xenforo userID. Lookup the user in Xenforo database user table
            try:
                xenforouser = XenforoUser.objects.using(settings.XENFORO['database']).get(pk=request.session['xf_user_id'])
            except XenforoUser.DoesNotExist:
                pass
            else:
                if xenforouser.user_state == 'valid' and xenforouser.is_banned not in (True, '1'):
                    # attempt to authenticate the user using our UserBackend.
                    user = auth.authenticate(request, xenforouser=xenforouser)
                    if user:
                        # User is valid.  Set request.user and persist user in the session
                        # by logging the user in.
                        request.user = user
                        auth.login(request, user)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
