# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_moduser_last_renew_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='moduser',
            name='date_of_expiration',
            field=models.DateField(default=datetime.datetime(2074, 1, 1, 0, 0)),
        ),
    ]
