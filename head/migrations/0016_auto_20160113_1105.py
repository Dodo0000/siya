# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('head', '0015_book_saved_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookSaver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='saved_by',
        ),
        migrations.AddField(
            model_name='book',
            name='saved_by',
            field=models.ManyToManyField(to='head.BookSaver', null=True, db_index=True),
        ),
    ]
