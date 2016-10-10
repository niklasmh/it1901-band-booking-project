# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 23:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('booking', '0015_auto_20161009_2003'), ('booking', '0016_auto_20161009_2148'), ('booking', '0017_auto_20161009_2151'), ('booking', '0018_auto_20161009_2155'), ('booking', '0019_bookingevent_time'), ('booking', '0020_auto_20161009_2228'), ('booking', '0021_bookingevent_user')]

    dependencies = [
        ('booking', '0014_auto_20161006_0925'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='offer_sent',
        ),
        migrations.AlterField(
            model_name='booking',
            name='state',
            field=models.CharField(choices=[(' ', '-'), ('r', 'Rejected'), ('a', 'Accepted'), ('c', 'Cancelled'), ('e', 'Offer sent'), ('b', 'Offer accepted'), ('d', 'Offer rejected')], default=' ', max_length=1),
        ),
        migrations.CreateModel(
            name='BookingEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.IntegerField(choices=[(0, 'Create'), (1, 'Transition')])),
                ('pre_transition_state', models.CharField(blank=True, choices=[(' ', '-'), ('r', 'Rejected'), ('a', 'Accepted'), ('c', 'Cancelled'), ('e', 'Offer sent'), ('b', 'Offer accepted'), ('d', 'Offer rejected'), ('x', 'Replaced')], max_length=1, null=True)),
                ('transition', models.CharField(blank=True, choices=[('a', 'Accept'), ('r', 'Reject'), ('o', 'Send offer'), ('m', 'Replace'), ('c', 'Cancel')], max_length=1, null=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='booking.Booking')),
                ('time', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='state',
            field=models.CharField(choices=[(' ', '-'), ('r', 'Rejected'), ('a', 'Accepted'), ('c', 'Cancelled'), ('e', 'Offer sent'), ('b', 'Offer accepted'), ('d', 'Offer rejected'), ('x', 'Replaced')], default=' ', max_length=1),
        ),
    ]
