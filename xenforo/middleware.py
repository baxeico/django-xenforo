from socket import inet_ntoa
from struct import pack
from time import time
import logging

from django.db import connections
from django.conf import settings
from django.utils.encoding import force_bytes

import phpserialize

from .models import XenforoUser

logger = logging.getLogger(__name__)

class XFSessionMiddleware(object):
    def process_request(self, request):
        request.xf_session_id = request.COOKIES.get(settings.XENFORO['cookie_prefix'] + 'session', None)
        request.xf_session = None

        if not request.xf_session_id:
            return

        # TODO: pluggable SessionStores
        cursor = connections[settings.XENFORO['database']].cursor()
        cursor.execute("SELECT session_id, session_data, expiry_date FROM " + settings.XENFORO['table_prefix'] + "session WHERE session_id = %s AND expiry_date >= %s",
            [request.xf_session_id, int(time())])
        row = cursor.fetchone()
        cursor.close()

        if row:
            request.xf_session = phpserialize.loads(force_bytes(row[1]), object_hook=phpserialize.phpobject)

class XFRemoteUserMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'xf_session'), "The XenForo authentication middleware requires the XF session middleware to be installed."

        if 'xenforo_username' in request.session:
            request.META['REMOTE_USER'] = request.session['xenforo_username']
            return

        if not request.xf_session:
            return

        if 'userId' not in request.xf_session:
            return

        try:
            lookup_user_id = int(request.xf_session.get('userId'))
        except:
            return

        try:
            xenforouser = XenforoUser.objects.using(settings.XENFORO['database']).get(pk=lookup_user_id)
        except XenforoUser.DoesNotExist:
            return

        if xenforouser.user_state == 'valid' and not xenforouser.is_banned:
            request.META['REMOTE_USER'] = xenforouser.username
            request.session['xenforo_username'] = xenforouser.username
