# coding=utf-8

from django.db import models
from django.conf import settings

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
