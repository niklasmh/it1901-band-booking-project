# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-09 22:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0020_auto_20161009_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingevent',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
