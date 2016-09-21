from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import model_to_dict
from booking import models, forms

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

class BookingUpdateView(PermissionRequiredMixin, CreateView, SingleObjectMixin):
	permission_required = 'booking.edit_booking'
	model = models.Booking
	pk_url_kwarg = 'booking'
	fields = ('band', 'venue', 'begin', 'end', 'band_fee', 'price_member', 'price')

	def dispatch(self, request, *args, **kwargs):
		self.object_original = self.get_object()
		return super(BookingUpdateView, self).dispatch(request, *args, **kwargs)

	def get_initial(self):
		return model_to_dict(self.object_original)

	def form_valid(self, form):
		form.instance.replaces = self.object_original
		form.instance.user = self.request.user
		res = super(BookingUpdateView, self).form_valid(form)
		if self.object_original.state == models.BOOKING_NONE:
			self.object_original.state = models.BOOKING_REPLACED
			self.object_original.save()
		return res

	def get_context_data(self, **kwargs):
		context = {}
		if self.object_original:
			context['object'] = self.object_original
			context_object_name = self.get_context_object_name(self.object_original)
			if context_object_name:
				context[context_object_name] = self.object_original
				context.update(kwargs)
		return super(BookingUpdateView, self).get_context_data(**context)

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

		if form.cleaned_data['accepted'] and form.cleaned_data['rejected']:
			return self.form_invalid(form)

		if form.cleaned_data['accepted']:
			booking.state = models.BOOKING_ACCEPTED
			replaces = booking.replaces
			if replaces:
				replaces.state = models.BOOKING_REPLACED
				replaces.save()
		elif form.cleaned_data['rejected']:
			booking.state = models.BOOKING_REJECTED
		booking.save()
		return super(BookingSetStateView, self).form_valid(form)

	def form_invalid(self, form):
		return HttpResponseRedirect(reverse('booking:detail', kwargs={'booking': self.kwargs['booking']}))

	def get_success_url(self):
		if self.object.state == 'a':
			return reverse('booking:detail', kwargs={'booking': self.kwargs['booking']})
		else:
			return reverse('booking:list')
