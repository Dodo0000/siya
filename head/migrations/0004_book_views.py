# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0003_auto_20160325_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
