import logging

from django.contrib.auth import get_user_model
from django.conf import settings

from .models import XenforoUser

logger = logging.getLogger(__name__)

class UserBackend(object):

    def get_user(self, user_id):
        try:
            UserModel = get_user_model()
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def authenticate(self, request, xenforouser):
        """
        The user passed as ``xenforouser`` is considered trusted and it's an instance of models.XenforoUser.
        This method returns the ``settings.AUTH_USER_MODEL`` object with the given username (and optionally the same xenforo_id),
        creating a new ``settings.AUTH_USER_MODEL`` object if it not already exists.
        """
        UserModel = get_user_model()
        lookup_params = { 'username': xenforouser.username }
        # if configured to take Xenforo User ID into account, add the id to the lookup fields
        save_xenforo_user_id = settings.XENFORO.get('save_xenforo_user_id')
        if save_xenforo_user_id:
            lookup_params['xenforo_id'] = xenforouser.id
        # if running with Sites framework turned on, take the Site into account
        if settings.SITE_ID:
            lookup_params['site_id'] = settings.SITE_ID
        user, created = UserModel.objects.get_or_create(**lookup_params,
            defaults={
                'email': xenforouser.email,
                'is_superuser': xenforouser.is_admin,
                'is_staff': xenforouser.is_staff
            })
        return user
