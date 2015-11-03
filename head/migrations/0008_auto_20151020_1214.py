# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0007_auto_20151020_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifter',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='gifter',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
