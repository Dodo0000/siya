# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0010_auto_20151118_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('book', models.ForeignKey(to='head.Book')),
            ],
        ),
    ]
