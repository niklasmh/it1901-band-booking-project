from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from band.models import Band
from venue.models import Venue
from django.utils import timezone
from datetime import date

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
	band = models.ForeignKey(Band, related_name='bookings')
	venue = models.ForeignKey(Venue, related_name='bookings')
	user = models.ForeignKey(User)
	begin = models.DateTimeField()
	end = models.DateTimeField()
	band_fee = models.DecimalField(max_digits=10, decimal_places=2)
	ticket_price_member = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ticket price member')
	ticket_price_non_member = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ticket price non-member')
	total_tickets_for_sale = models.IntegerField()
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

	def is_past_due(self):
		if date.today() > self.begin.date():
			return True
		return False

	def state_accepted(self):
		if self.state == BOOKING_ACCEPTED:
			return True
		return False

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
	ticket_sold_member = models.IntegerField()
	ticket_sold_non_member = models.IntegerField()
	additional_information = models.TextField(blank=True)

	def sum_member_tickets(self):
		return self.ticket_sold_member * self.booking.ticket_price_member
	def sum_non_member_tickets(self):
		return self.ticket_sold_non_member * self.booking.ticket_price_non_member
	def sum_tickets(self):
		return self.sum_member_tickets() + self.sum_non_member_tickets()

	def sum_income(self):
		return self.sum_tickets()
	def sum_expences(self):
		return self.booking.band_fee
	def sum(self):
		return self.sum_income() - self.sum_expences()

	def get_absolute_url(self):
			return reverse('booking:detail', kwargs={ 'booking': self.booking.id })

#skriv inn scenearbeidere her:
