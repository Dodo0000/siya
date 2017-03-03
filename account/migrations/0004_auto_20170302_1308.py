# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_moduser_date_of_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduser',
            name='date_of_expiration',
            field=models.DateField(),
        ),
    ]
