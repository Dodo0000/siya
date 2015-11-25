# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0014_auto_20151125_2330'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GenericFieldBookLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(null=True)),
                ('book', models.ForeignKey(to='head.Book')),
            ],
        ),
        migrations.AddField(
            model_name='genericfield',
            name='value',
            field=models.ManyToManyField(to='miscFields.GenericFieldBookLink'),
        ),
    ]
