from django.db import models
from venue.models import Venue
from booking.models import Booking
from django.contrib.auth.models import User

class Group(models.Model):
	name = models.CharField(max_length=200)
	members = models.ManyToManyField(User, related_name='shift_groups')

class Shift(models.Model):
	booking = models.ForeignKey(Booking, related_name='shifts')
	user = models.ForeignKey(User, blank=True, null=True, related_name='shifts')
	name = models.CharField(max_length=200)

class DefaultShiftSet(models.Model):
	venue = models.ForeignKey(Venue, related_name='shiftsets')
	name = models.CharField(max_length=200)

class DefaultShift(models.Model):
	shiftset = models.ForeignKey(DefaultShiftSet, related_name='shifts')
	name = models.CharField(max_length=200)
