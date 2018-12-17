# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('log_type', models.SmallIntegerField(choices=[(0, 'login'), (1, 'logout'), (2, 'cmd')])),
                ('content', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('host2remote_user', models.ForeignKey(to='web.Host2RemoteUser')),
                ('user', models.ForeignKey(verbose_name='堡垒机用户', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
