# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20170302_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduser',
            name='date_of_expiration',
            field=models.DateField(null=True, blank=True),
        ),
    ]
