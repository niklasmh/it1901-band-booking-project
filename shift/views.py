from django.views.generic import ListView, DetailView, CreateView, UpdateView
from shift import models
from booking import models as booking
import datetime

class ShiftListView(ListView):
	model = models.Shift

	def get_queryset(self):
		qs = super(ShiftListView, self).get_queryset()
		qs = qs.filter(user=self.request.user)
		qs = qs.filter(booking__state=booking.BOOKING_OFFER_ACCEPTED)
		qs = qs.filter(booking__end__gt=datetime.date.today())
		return qs
