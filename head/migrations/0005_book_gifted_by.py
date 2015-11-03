# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0004_remove_book_gifted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='gifted_by',
            field=models.ForeignKey(to='head.Gifter', null=True),
        ),
    ]
