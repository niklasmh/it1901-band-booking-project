# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-01 16:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0015_auto_20161027_0910'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='band',
            options={'permissions': (('view_managing_bands', 'View managing bands'), ('view_booking', 'View booking'))},
        ),
    ]