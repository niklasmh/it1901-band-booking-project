from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from band.models import Band
from venue.models import Venue
from django.utils import timezone

BOOKING_NONE = ' '
BOOKING_REJECTED = 'r'
BOOKING_ACCEPTED = 'a'
BOOKING_CANCELLED = 'c'
BOOKING_REPLACED = 'm'
BOOKING_FINISHED = 'f'
BOOKING_CHOICES = (
	(BOOKING_NONE, '-'),
	(BOOKING_REJECTED, 'Rejected'),
	(BOOKING_ACCEPTED, 'Accepted'),
	(BOOKING_CANCELLED, 'Cancelled'),
	(BOOKING_REPLACED, 'Replaced'),
)

class Booking(models.Model):
	band = models.ForeignKey(Band)
	venue = models.ForeignKey(Venue)
	user = models.ForeignKey(User)
	begin = models.DateTimeField()
	end = models.DateTimeField()
	band_fee = models.DecimalField(max_digits=10, decimal_places=2)
	price_member = models.DecimalField(max_digits=10, decimal_places=2)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	state = models.CharField(max_length=1, default=' ', choices=BOOKING_CHOICES)
	replaces = models.ForeignKey('Booking', null=True, blank=True, related_name='replacements')

	def __str__(self):
		return "%s @ %s" % (self.band, self.venue)

	def get_absolute_url(self):
		return reverse('booking:detail', kwargs={ 'booking': self.id })

	def report_ready(self):
		return self.state=='a' and self.end < timezone.now()

	class Meta:
		permissions = (
			("accept_booking", "Accept or reject booking"),
		)

class Report(models.Model):
	booking = models.OneToOneField(
		Booking,
		on_delete=models.CASCADE,
		related_name="report",
	)
	attended_member = models.IntegerField()
	attended_non_member = models.IntegerField()
	additional_information = models.TextField(blank=True)

	def get_absolute_url(self):
			return reverse('booking:detail', kwargs={ 'booking': self.booking.id })

#skriv inn scenearbeidere her:
