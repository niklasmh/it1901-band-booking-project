# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='price',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='price_member',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
