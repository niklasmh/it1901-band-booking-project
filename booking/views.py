from django.views.generic import ListView, DetailView, CreateView, UpdateView
from booking import models

class BookingListView(ListView):
	model = models.Booking

class BookingDetailView(DetailView):
	model = models.Booking
	pk_url_kwarg = 'booking'

class BookingCreateView(CreateView):
	model = models.Booking
	fields = ('band', 'venue', 'begin', 'end', 'band_fee', 'price_member', 'price')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(BookingCreateView, self).form_valid(form);
