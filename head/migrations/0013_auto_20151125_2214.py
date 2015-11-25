# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0012_auto_20151125_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericfieldbooklink',
            name='value',
            field=models.TextField(null=True),
        ),
    ]
