from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import model_to_dict
from booking import models, forms
from datetime import datetime, date, timedelta
import re

def get_week_number(date):
	return date.strftime('%Y-W%W')

def get_weekspan(date):
	weeklist_begin = date - timedelta(days=date.weekday())
	weeklist_end = weeklist_begin + timedelta(days=7)
	return weeklist_begin, weeklist_end

def get_weekspan_from_number(week, year):
	weeklist_begin = datetime.strptime("%s-W%s-1" % (year, week), "%Y-W%W-%w")
	weeklist_end = weeklist_begin + timedelta(days=7)
	return weeklist_begin, weeklist_end

class BookingListView(ListView):
	model = models.Booking

	def get_context_data(self, **kwargs):
		context = super(BookingListView, self).get_context_data(**kwargs)
		today = date.today()

		weeklist_begin, weeklist_end = get_weekspan(today)
		if 'week' in self.request.GET:
			m = re.match("([0-9]{4})-W([0-9]+)", self.request.GET.get('week'))
			if m:
				year, week = m.group(1, 2)
				weeklist_begin, weeklist_end = get_weekspan_from_number(week, year)
		context['weeklist'] = {
			'week': (weeklist_begin),
			'week_next': (weeklist_begin + timedelta(days=7)),
			'week_previous': (weeklist_begin - timedelta(days=7)),
			'list': self.model.objects.filter(state__in=(models.BOOKING_ACCEPTED, models.BOOKING_NONE),
											  begin__range=(weeklist_begin, weeklist_end)),
		}
		return context

	def get_queryset(self):
		qs = super(BookingListView, self).get_queryset()
		if 'date' in self.request.GET:
			qs = qs.filter(begin__date=datetime.strptime(self.request.GET.get('date'), '%Y-%m-%d'))
		if 'venue' in self.request.GET:
			try:
				i = int(self.request.GET.get('venue'))
				qs = qs.filter(venue__id=i)
			except ValueError:
				qs = qs.filter(venue__slug=self.request.GET.get('venue'))
		return qs

class BookingDetailView(DetailView):
	model = models.Booking
	pk_url_kwarg = 'booking'

class BookingCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'booking.add_booking'
	model = models.Booking
	fields = ('band', 'venue', 'begin', 'end', 'band_fee', 'price_member', 'price')

	def get_initial(self):
		initial = {}
		if 'date' in self.request.GET:
			initial['begin'] = datetime.strptime(self.request.GET.get('date') + " 18:00", '%Y-%m-%d %H:%M')
			initial['end'] = datetime.strptime(self.request.GET.get('date') + " 20:00", '%Y-%m-%d %H:%M')
		if 'venue' in self.request.GET:
			q = {'slug': self.request.GET.get('venue')}
			try:
				i = int(self.request.GET.get('venue'))
				q = {'id': i}
			except ValueError:
				pass
			initial['venue'] = models.Venue.objects.get(**q)
		return initial

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(BookingCreateView, self).form_valid(form)
    
class BookingReportCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'booking.add_report'
	model = models.Report
	fields = ('attended_member', 'attended', 'additional_information')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(BookingReportCreateView, self).form_valid(form)

class BookingUpdateView(PermissionRequiredMixin, CreateView, SingleObjectMixin):
	permission_required = 'booking.edit_booking'
	model = models.Booking
	pk_url_kwarg = 'booking'
	fields = ('band', 'venue', 'begin', 'end', 'band_fee', 'price_member', 'price')

	def dispatch(self, request, *args, **kwargs):
		self.object_original = self.get_object()
		if self.object_original.state == models.BOOKING_REPLACED:
			messages.warning(self.request, 'The booking has already been %s.' % (
				self.object_original.get_state_display()
			))
			return HttpResponseRedirect(reverse('booking:detail',
												kwargs={'booking': self.object_original.id}))
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
