from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from band.models import Band
from venue.models import Venue

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
	state = models.CharField(max_length=1, default=' ', choices=((' ', '-'),
																 ('r', 'Rejected'),
																 ('a', 'Accepted')))

	def __str__(self):
		return "%s @ %s" % (self.band, self.venue)

	def get_absolute_url(self):
		return reverse('booking:detail', kwargs={ 'booking': self.id })

	class Meta:
		permissions = (
			("accept_booking", "Accept or reject booking"),
		)
