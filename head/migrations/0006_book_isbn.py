# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0005_book_gifted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
