# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0005_band_concerts'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='sold_albums',
            field=models.IntegerField(default=0),
        ),
    ]