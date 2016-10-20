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
BOOKING_FINISHED = 'f'
BOOKING_OFFER_SENT = 'e'
BOOKING_OFFER_ACCEPTED = 'b'
BOOKING_OFFER_REJECTED = 'd'
BOOKING_REPLACED = 'x'
BOOKING_CANCEL = 'm'

BOOKING_TRANSITION_ACCEPT = 'a'
BOOKING_TRANSITION_REJECT = 'r'
BOOKING_TRANSITION_SEND_OFFER = 'o'
BOOKING_TRANSITION_REPLACE = 'm'
BOOKING_TRANSITION_CANCEL = 'c'

BOOKING_CHOICES = (
	(BOOKING_NONE, '-'),
	(BOOKING_REJECTED, 'Rejected'),
	(BOOKING_ACCEPTED, 'Accepted'),
	(BOOKING_CANCELLED, 'Cancelled'),
	(BOOKING_OFFER_SENT, 'Offer sent'),
	(BOOKING_OFFER_ACCEPTED, 'Offer accepted'),
	(BOOKING_OFFER_REJECTED, 'Offer rejected'),
	(BOOKING_REPLACED, 'Replaced'),
)

BOOKING_TRANSITION_CHOICES = (
	(BOOKING_TRANSITION_ACCEPT, 'Accept'),
	(BOOKING_TRANSITION_REJECT, 'Reject'),
	(BOOKING_TRANSITION_SEND_OFFER, 'Send offer'),
	(BOOKING_TRANSITION_REPLACE, 'Replace'),
	(BOOKING_TRANSITION_CANCEL, 'Cancel'),
)

BOOKING_IS_ACCEPTED = (
	BOOKING_ACCEPTED, BOOKING_OFFER_SENT, BOOKING_OFFER_ACCEPTED
)

BOOKING_STATEMACHINE = {
	(BOOKING_NONE, BOOKING_TRANSITION_ACCEPT): BOOKING_ACCEPTED,
	(BOOKING_NONE, BOOKING_TRANSITION_REJECT): BOOKING_REJECTED,
	(BOOKING_ACCEPTED, BOOKING_TRANSITION_SEND_OFFER): BOOKING_OFFER_SENT,
	(BOOKING_OFFER_SENT, BOOKING_TRANSITION_ACCEPT): BOOKING_OFFER_ACCEPTED,
	(BOOKING_OFFER_SENT, BOOKING_TRANSITION_REJECT): BOOKING_OFFER_REJECTED,

	(BOOKING_NONE, BOOKING_TRANSITION_CANCEL): BOOKING_CANCELLED,
	(BOOKING_ACCEPTED, BOOKING_TRANSITION_CANCEL): BOOKING_CANCELLED,
	(BOOKING_OFFER_SENT, BOOKING_TRANSITION_CANCEL): BOOKING_CANCELLED,
	(BOOKING_OFFER_ACCEPTED, BOOKING_TRANSITION_CANCEL): BOOKING_CANCELLED,

	(BOOKING_NONE, BOOKING_TRANSITION_REPLACE): BOOKING_REPLACED,
	(BOOKING_REJECTED, BOOKING_TRANSITION_REPLACE): BOOKING_REPLACED,
	(BOOKING_ACCEPTED, BOOKING_TRANSITION_REPLACE): BOOKING_REPLACED,
	(BOOKING_OFFER_SENT, BOOKING_TRANSITION_REPLACE): BOOKING_REPLACED,
	(BOOKING_OFFER_REJECTED, BOOKING_TRANSITION_REPLACE): BOOKING_REPLACED,
	(BOOKING_OFFER_ACCEPTED, BOOKING_TRANSITION_REPLACE): BOOKING_REPLACED,
	(BOOKING_REPLACED, BOOKING_TRANSITION_REPLACE): BOOKING_REPLACED,
}

def get_name_from_choices(choices, value):
	return next(val for key, val in choices if key == value)

class InvalidTransition(Exception):
	def __init__(self, state, transition):
		self.state = state
		self.transition = transition
	def __str__(self):
		return "Invalid transition '%(transition)s' from state '%(state)s'" % {
			'state': self.state, 'transition': self.transition
		}

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

	def state_transition(self, transition, user=None):
		old_state = self.state
		new_state = self.state_transition_legal(transition)
		if user is None:
			user = self.user
		if new_state:
			self.state = new_state
			self.save()
			event = BookingEvent(booking=self,
								 event_type=BOOKING_EVENT_TRANSITION,
								 pre_transition_state=old_state,
								 transition=transition,
								 user=user)
			event.save()
		else:
			raise InvalidTransition(*tr)
	def state_transition_legal(self, transition):
		return BOOKING_STATEMACHINE.get((self.state, transition), None)

	def get_absolute_url(self):
		return reverse('booking:detail', kwargs={ 'booking': self.id })

	def report_ready(self):
		return self.state=='b' and self.end < timezone.now()

	def is_past_due(self):
		return date.today() > self.begin.date()

	def state_accepted(self):
		return self.state == BOOKING_ACCEPTED

	def check_offer_sent(self):
		if self.offer_sent == False:
			self.offer_sent = True
			return True
		elif self.offer_sent == True:
			return False
		return False

	class Meta:
		permissions = (
			("accept_booking", "Accept or reject booking"),
		)

BOOKING_EVENT_CREATE = 0
BOOKING_EVENT_TRANSITION = 1
BOOKING_EVENT_CHOICES = (
	(BOOKING_EVENT_CREATE, 'Create'),
	(BOOKING_EVENT_TRANSITION, 'Transition'),
)

class BookingEvent(models.Model):
	booking = models.ForeignKey(
		Booking,
		on_delete=models.CASCADE,
		related_name="events"
	)
	event_type = models.IntegerField(choices=BOOKING_EVENT_CHOICES)
	pre_transition_state = models.CharField(choices=BOOKING_CHOICES, null=True, blank=True, max_length=1)
	transition = models.CharField(choices=BOOKING_TRANSITION_CHOICES, null=True, blank=True, max_length=1)
	time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User)

	def __str__(self):
		print("Booking transitioned from state %(state_from) to state %(state_to) by %(trans)")
		return {
			BOOKING_EVENT_CREATE: lambda i: "Booking created",
			BOOKING_EVENT_TRANSITION: lambda i: "Booking transitioned from state %(state_from)s to state %(state_to)s by %(trans)s" % {
				'state_from': get_name_from_choices(BOOKING_CHOICES, i.pre_transition_state),
				'state_to': get_name_from_choices(
					BOOKING_CHOICES,
					BOOKING_STATEMACHINE[(i.pre_transition_state, i.transition)]),
				'trans': get_name_from_choices(BOOKING_TRANSITION_CHOICES, i.transition),
			},
		}[self.event_type](self)

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

class Technical_Requirements(models.Model):
	booking = models.OneToOneField(
		Booking,
		on_delete=models.CASCADE,
		related_name="tech_req"
	)
	requirements = models.TextField()

	def get_absolute_url(self):
			return reverse('booking:detail', kwargs={ 'booking': self.booking.id })
