# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=90, null=True)),
                ('last_name', models.CharField(max_length=90, null=True)),
                ('username', models.CharField(unique=True, max_length=25)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date Joined')),
                ('gender', models.CharField(max_length=6, null=True, choices=[(b'male', b'male'), (b'female', b'female')])),
                ('age', models.PositiveIntegerField(null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_type', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.AddField(
            model_name='moduser',
            name='user_type',
            field=models.ForeignKey(to='account.UserType'),
        ),
    ]
