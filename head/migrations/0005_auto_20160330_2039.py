# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0004_book_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
