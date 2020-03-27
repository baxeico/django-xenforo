# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XenforoUser',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, db_column=b'user_id')),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=120)),
                ('user_state', models.CharField(max_length=50)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_banned', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'xf_user',
                'managed': False,
            },
        ),
    ]
