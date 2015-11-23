# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='accent_color',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='primary_color',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='accent_color',
            field=models.CharField(default=b'eeeeee', max_length=6),
        ),
        migrations.AlterField(
            model_name='organization',
            name='primary_color',
            field=models.CharField(default=b'1c6585', max_length=6),
        ),
    ]
