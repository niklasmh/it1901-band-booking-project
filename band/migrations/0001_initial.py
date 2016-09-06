# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-06 23:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact_person', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=30, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=30, null=True)),
                ('spotify_artist_id', models.CharField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
