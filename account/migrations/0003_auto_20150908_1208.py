# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_moduser_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moduser',
            name='age',
        ),
        migrations.AddField(
            model_name='moduser',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
