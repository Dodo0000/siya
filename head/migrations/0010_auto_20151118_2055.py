# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0009_auto_20151020_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='accession_number',
            field=models.CharField(max_length=9, db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='accessioned_date',
            field=models.DateField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(to='head.Author', db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='call_number',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.CharField(db_index=True, max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=13, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='keywords',
            field=models.ManyToManyField(to='head.KeyWord', db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(default=b'EN', max_length=5, db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='no_of_pages',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='series',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='state',
            field=models.IntegerField(default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='volume',
            field=models.CharField(db_index=True, max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gifter',
            name='date_given',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='lend',
            name='borrowed',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='lend',
            name='lending_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='lend',
            name='returned',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='lend',
            name='returned_date',
            field=models.DateField(null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='place',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='year',
            field=models.CharField(max_length=10, db_index=True),
        ),
    ]
