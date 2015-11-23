# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primary_color', models.CharField(max_length=6)),
                ('accent_color', models.CharField(max_length=6)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'My Awesome Library', max_length=255)),
                ('motto', models.TextField(null=True)),
                ('no_of_books_at_once', models.IntegerField(default=2)),
                ('no_of_days_to_borrow', models.IntegerField(default=10)),
                ('rate_of_late_fees', models.FloatField(default=2)),
                ('primary_color', models.CharField(max_length=6)),
                ('accent_color', models.CharField(max_length=6)),
                ('members', models.ManyToManyField(to='configurations.Individual')),
            ],
        ),
    ]
