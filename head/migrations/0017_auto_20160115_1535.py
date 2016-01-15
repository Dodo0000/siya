# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0016_auto_20160113_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='saved_by',
            field=models.ManyToManyField(default=django.utils.timezone.now, to='head.BookSaver', db_index=True),
        ),
    ]
