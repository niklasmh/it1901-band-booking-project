# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0005_auto_20161004_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='genres',
            field=models.ManyToManyField(null=True, to='band.Genre'),
        ),
    ]
