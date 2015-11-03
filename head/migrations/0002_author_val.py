# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='val',
            field=models.IntegerField(default=12),
        ),
    ]
