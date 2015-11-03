# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0003_remove_author_val'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='gifted_by',
        ),
    ]
