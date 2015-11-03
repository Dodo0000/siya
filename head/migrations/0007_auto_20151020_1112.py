# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0006_book_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifter',
            name='date_given',
            field=models.DateField(),
        ),
    ]
