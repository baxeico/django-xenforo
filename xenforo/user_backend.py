import logging

from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth import get_user_model

from .models import XenforoUser

logger = logging.getLogger(__name__)

class UserBackend(RemoteUserBackend):

    def get_user(self, user_id):
        try:
            UserModel = get_user_model()
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def authenticate(self, remote_user):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``settings.AUTH_USER_MODEL`` object with the given username,
        creating a new ``settings.AUTH_USER_MODEL`` object if it not already exists.
        """
        if not remote_user:
            return
        username = self.clean_username(remote_user)
        UserModel = get_user_model()
        user, created = UserModel.objects.get_or_create(username=username)
        if created:
            user = self.configure_user(user)
        return user

    def configure_user(self, user):
        """
        Get some info from Xenforo user and save them on Django user
        """
        try:
            xenforouser = XenforoUser.objects.using(settings.XENFORO['database']).get(username=user.username)
        except XenforoUser.DoesNotExist:
            logger.error('Unable to find Xenforo user with username %s' % user.username)
        else:
            user.email = xenforouser.email
            user.is_superuser = xenforouser.is_admin
            user.is_staff = xenforouser.is_staff
            user.save()
        return user