# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auditlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildrenTaskResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('result', models.TextField(verbose_name='任务执行结果')),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'initialized'), (1, 'sucess'), (2, 'failed'), (3, 'timeout')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('host2remote_user', models.ForeignKey(to='web.Host2RemoteUser')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('task_type', models.CharField(choices=[('cmd', '批量命令'), ('file-transfer', '文件传输')], max_length=64)),
                ('content', models.CharField(verbose_name='任务内容', max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='childrentaskresult',
            name='task',
            field=models.ForeignKey(to='web.Task'),
        ),
    ]
