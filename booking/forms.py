from django import forms
from booking import models
from venue.models import Venue

class BookingForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.original_booking = kwargs.pop('original_booking', None)
		super(BookingForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super(BookingForm, self).clean()
		errors = []
		venue = cleaned_data['venue']
		begin = cleaned_data['begin']
		end = cleaned_data['end']

		if begin > end:
			errors.append(forms.ValidationError(
				"The event cannot end before it starts."
			))

		qs = models.Booking.objects.filter(venue=venue,
										   begin__date=begin.date(),
										   state__in=(models.BOOKING_ACCEPTED))
		if self.original_booking:
			qs = qs.exclude(id=self.original_booking.id)

		if len(qs) > 0:
			errors.append(forms.ValidationError(
				"The venue %(venue)s is already in use on this day.",
				params={'venue': venue}
			))
		if errors:
			raise forms.ValidationError(errors)
		return cleaned_data
	class Meta:
		model = models.Booking
		fields = ('band', 'venue', 'begin', 'end', 'band_fee', 'price_member', 'price')

class BookingSetStateForm(forms.Form): 
    accepted = forms.BooleanField(required = False) 
    rejected = forms.BooleanField(required = False) 
