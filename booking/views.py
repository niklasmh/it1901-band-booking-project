from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from booking import models,forms

class BookingListView(ListView):
	model = models.Booking

class BookingDetailView(DetailView):
	model = models.Booking
	pk_url_kwarg = 'booking'

class BookingCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'booking.add_booking'
	model = models.Booking
	fields = ('band', 'venue', 'begin', 'end', 'band_fee', 'price_member', 'price')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(BookingCreateView, self).form_valid(form);

class BookingSetStateView(PermissionRequiredMixin, FormView):
	permission_required = 'booking.accept_booking'
	form_class = forms.BookingSetStateForm

	def get(self, request, booking, **kwargs):
		return HttpResponseRedirect(reverse('booking:detail', kwargs={'booking': booking}))

	def form_valid(self, form):
		booking = models.Booking.objects.get(id = self.kwargs["booking"])
		self.object = booking
		if booking.state != ' ':
			messages.warning(self.request, 'The booking has already been %s.' % booking.get_state_display())
			return self.form_invalid(form)
		booking.state = "a" if form.cleaned_data["accepted"] else "r"
		booking.save()
		return super(BookingSetStateView, self).form_valid(form)

	def form_invalid(self, form):
		return HttpResponseRedirect(reverse('booking:detail', kwargs={'booking': self.kwargs['booking']}))

	def get_success_url(self):
		if self.object.state == 'a':
			return reverse('booking:detail', kwargs={'booking': self.kwargs['booking']})
		else:
			return reverse('booking:list')
