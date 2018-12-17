# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(max_length=255, verbose_name='email address', unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(to='auth.Group', related_query_name='user', verbose_name='groups', related_name='user_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('port', models.SmallIntegerField(default=22)),
            ],
        ),
        migrations.CreateModel(
            name='Host2RemoteUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('host', models.ForeignKey(to='web.Host')),
            ],
        ),
        migrations.CreateModel(
            name='HostCroup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('host2remote_users', models.ManyToManyField(to='web.Host2RemoteUser')),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('auth_type', models.SmallIntegerField(choices=[(0, 'ssh-password'), (1, 'ssh-key')], default=0)),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=64, blank=True, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='remoteuser',
            unique_together=set([('auth_type', 'username', 'password')]),
        ),
        migrations.AddField(
            model_name='host2remoteuser',
            name='remote_user',
            field=models.ForeignKey(to='web.RemoteUser'),
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(to='web.IDC'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='host2remote_users',
            field=models.ManyToManyField(to='web.Host2RemoteUser', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='host_groups',
            field=models.ManyToManyField(to='web.HostCroup', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', related_query_name='user', verbose_name='user permissions', related_name='user_set', blank=True, help_text='Specific permissions for this user.'),
        ),
        migrations.AlterUniqueTogether(
            name='host2remoteuser',
            unique_together=set([('host', 'remote_user')]),
        ),
    ]
