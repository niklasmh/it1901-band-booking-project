# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-27 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_auto_20160927_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='state',
            field=models.CharField(choices=[(' ', '-'), ('r', 'Rejected'), ('a', 'Accepted'), ('c', 'Cancelled'), ('m', 'Replaced')], default=' ', max_length=1),
        ),
    ]
