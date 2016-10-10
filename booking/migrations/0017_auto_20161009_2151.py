# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-09 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_auto_20161009_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='state',
            field=models.CharField(choices=[(' ', '-'), ('r', 'Rejected'), ('a', 'Accepted'), ('c', 'Cancelled'), ('e', 'Offer sent'), ('b', 'Offer accepted'), ('d', 'Offer rejected'), ('x', 'Replaced')], default=' ', max_length=1),
        ),
        migrations.AlterField(
            model_name='bookingevent',
            name='pre_transition_state',
            field=models.CharField(blank=True, choices=[(' ', '-'), ('r', 'Rejected'), ('a', 'Accepted'), ('c', 'Cancelled'), ('e', 'Offer sent'), ('b', 'Offer accepted'), ('d', 'Offer rejected'), ('x', 'Replaced')], max_length=1, null=True),
        ),
    ]
