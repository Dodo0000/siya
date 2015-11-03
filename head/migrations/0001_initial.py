# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accession_number', models.CharField(max_length=9)),
                ('accessioned_date', models.DateField(auto_now=True)),
                ('call_number', models.CharField(max_length=20, null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('no_of_pages', models.IntegerField()),
                ('language', models.CharField(default=b'EN', max_length=5)),
                ('series', models.CharField(max_length=20, null=True, blank=True)),
                ('edition', models.CharField(max_length=100, null=True, blank=True)),
                ('price', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.CharField(max_length=10, null=True, blank=True)),
                ('state', models.IntegerField(default=0)),
                ('author', models.ManyToManyField(to='head.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Gifter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_given', models.DateField(auto_now=True)),
                ('gifter_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Lend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lending_date', models.DateField()),
                ('returned_date', models.DateField(null=True)),
                ('returned', models.BooleanField(default=False)),
                ('borrowed', models.BooleanField(default=False)),
                ('book', models.ForeignKey(to='head.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('place', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='gifted_by',
            field=models.ForeignKey(to='head.Gifter'),
        ),
        migrations.AddField(
            model_name='book',
            name='keywords',
            field=models.ManyToManyField(to='head.KeyWord'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(blank=True, to='head.Publisher', null=True),
        ),
    ]
