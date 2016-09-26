# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20160922_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended_member', models.IntegerField()),
                ('attended', models.IntegerField()),
                ('additional_information', models.TextField(blank=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='booking.Booking')),
            ],
        ),
        migrations.RemoveField(
            model_name='rapport',
            name='booking',
        ),
        migrations.DeleteModel(
            name='Rapport',
        ),
    ]
