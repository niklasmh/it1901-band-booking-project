from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
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

class BookingSetStateView(FormView):

    form_class = forms.BookingSetStateForm

    def form_valid(self, form):
        booking = models.Booking.objects.get(id = self.kwargs["booking"])
        booking.state = "a" if form.cleaned_data["accepted"] else "r"
        booking.save()
        return super(BookingSetStateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('booking:list')
