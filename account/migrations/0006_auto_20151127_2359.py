# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_moduser_school_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduser',
            name='addr_municipality',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='addr_tole',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='addr_ward_no',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='first_name',
            field=models.CharField(max_length=90, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='last_name',
            field=models.CharField(max_length=90, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='parent_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='parent_telephone_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='school_class',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='school_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='school_roll_no',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='school_telephone',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='telephone_home',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='telephone_mobile',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='moduser',
            name='username',
            field=models.CharField(unique=True, max_length=25, blank=True),
        ),
    ]
