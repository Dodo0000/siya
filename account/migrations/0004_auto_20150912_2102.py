# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150908_1208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moduser',
            old_name='gender',
            new_name='sex',
        ),
        migrations.RemoveField(
            model_name='moduser',
            name='description',
        ),
        migrations.RemoveField(
            model_name='moduser',
            name='user_type',
        ),
        migrations.AddField(
            model_name='moduser',
            name='addr_municipality',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='addr_tole',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='addr_ward_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='parent_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='parent_telephone_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='school_class',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='school_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='school_roll_no',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='school_varified',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='moduser',
            name='telephone_home',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='moduser',
            name='telephone_mobile',
            field=models.IntegerField(null=True),
        ),
    ]
