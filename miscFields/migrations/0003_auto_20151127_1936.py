# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscFields', '0002_auto_20151126_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericfield',
            name='key',
            field=models.CharField(default=b'What is My name?', max_length=255),
        ),
    ]
