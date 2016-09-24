from django import template
from django.utils import timezone
from datetime import datetime, timedelta
from booking import models

register = template.Library()



@register.filter
def weeklist(value, week):
	first_day = datetime.strptime("%s-1" % week, "%Y-W%W-%w")
	res = [{'date': first_day + timedelta(days=i), 'list': [] } for i in range(0, 7)]
	for entry in value:
		diff = (entry.begin.date() - first_day.date()).days
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
		
	print(res)
	return res.values()

@register.filter
def booking_weeklist(value, week):
	first_day = datetime.strptime("%s-1" % week, "%Y-W%W-%w")
	res = [{'date': first_day + timedelta(days=i), 'list': [], 'accepted': False, 'pending': False } for i in range(0, 7)]
	for entry in value:
		if not entry.state in (models.BOOKING_ACCEPTED, models.BOOKING_NONE):
			continue
		diff = (entry.begin.date() - first_day.date()).days
		if diff >= 7 or diff < 0:
			continue
		if entry.state == models.BOOKING_ACCEPTED:
			res[diff]['accepted'] = True
			res[diff]['booking'] = entry
		elif entry.state == models.BOOKING_NONE:
			res[diff]['pending'] = True
			res[diff]['list'].append(entry)
	return res

@register.filter
def weekdays(value, week):
	first_day = datetime.strptime("%s-1" % week, "%Y-W%W-%w")
	res = [first_day + timedelta(days=i) for i in range(0, 7)]
	return res
