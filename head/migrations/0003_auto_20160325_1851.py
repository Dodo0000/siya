# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0002_book_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='rating',
            new_name='votes',
        ),
    ]
