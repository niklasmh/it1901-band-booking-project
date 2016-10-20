from django import template
from django.utils import timezone
from datetime import datetime, timedelta
from booking import models
import re

register = template.Library()

def first_day_of_week(lhs):
	r = lhs - timedelta(days=lhs.weekday())
	if type(r) is datetime:
		r = r.date()
	return r

@register.filter
def weeklist(value, week):
	first_day = first_day_of_week(week)
	res = [{'date': first_day + timedelta(days=i), 'list': [] } for i in range(0, 7)]
	for entry in value:
		diff = (entry.begin.date() - first_day).days
		res[diff]['list'].append(entry)
	return res

@register.filter
def booking_venue_list(bookings):
	res = {}
	for venue in models.Venue.objects.filter(active=True):
		res[venue.id] = {
			'venue': venue,
			'booking_list': bookings.filter(venue=venue),
		}
		
	return res.values()

@register.filter
def booking_weeklist(value, week):
	first_day = first_day_of_week(week)
	res = [{
		'date': first_day + timedelta(days=i),
		'list': [],
		'accepted': False,
		'pending': False
	} for i in range(0, 7)]
	for entry in value:
		if not entry.state in models.BOOKING_IS_ACCEPTED + (models.BOOKING_NONE,):
			continue
		diff = (entry.begin.date() - first_day).days
		if diff >= 7 or diff < 0:
			continue
		if entry.state == models.BOOKING_ACCEPTED:
			res[diff]['accepted'] = True
			res[diff]['booking'] = entry
		elif entry.state == models.BOOKING_OFFER_ACCEPTED:
			res[diff]['offer_accepted'] = True
			res[diff]['booking'] = entry
		elif entry.state == models.BOOKING_OFFER_SENT:
			res[diff]['offer_sent'] = True
			res[diff]['booking'] = entry
		elif entry.state == models.BOOKING_NONE:
			res[diff]['pending'] = True
			res[diff]['list'].append(entry)
	return res

@register.filter
def weekdays(value, week):
	first_day = first_day_of_week(week)
	res = [first_day + timedelta(days=i) for i in range(0, 7)]
	return res
