# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0011_genericfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericFieldBookLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('book', models.ForeignKey(to='head.Book')),
            ],
        ),
        migrations.RemoveField(
            model_name='genericfield',
            name='book',
        ),
        migrations.RemoveField(
            model_name='genericfield',
            name='value',
        ),
        migrations.AddField(
            model_name='genericfield',
            name='value',
            field=models.ManyToManyField(to='head.GenericFieldBookLink'),
        ),
    ]
