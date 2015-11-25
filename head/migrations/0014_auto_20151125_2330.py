# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0013_auto_20151125_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericfield',
            name='value',
        ),
        migrations.RemoveField(
            model_name='genericfieldbooklink',
            name='book',
        ),
        migrations.DeleteModel(
            name='GenericField',
        ),
        migrations.DeleteModel(
            name='GenericFieldBookLink',
        ),
    ]
