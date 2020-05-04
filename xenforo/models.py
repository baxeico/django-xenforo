# coding=utf-8

from django.db import models
from django.conf import settings
from django.utils.encoding import force_bytes

import phpserialize

class XenforoUser(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=120)
    user_state = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        db_table = settings.XENFORO['table_prefix'] + 'user'
        managed = False

class XenforoSession(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='session_id')
    session_data = models.TextField()
    expiry_date = models.PositiveIntegerField()

    class Meta:
        db_table = settings.XENFORO['table_prefix'] + 'session'
        managed = False

    def get_session_data(self):
        return phpserialize.loads(force_bytes(self.session_data), object_hook=phpserialize.phpobject)
