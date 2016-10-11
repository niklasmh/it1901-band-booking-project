from django.template import Library
from django.utils.safestring import mark_safe
from django.utils.http import urlencode

register = Library()

@register.simple_tag
def keep_get_params(request, blacklist=''):
	blacklist = blacklist.split(',')
	inputs = ''
	for key in request.GET:
		if key in blacklist:
			continue
		for value in request.GET.getlist(key):
			inputs += '<input type="hidden" name="%s" value="%s"/>' % (
				key, value)
	return mark_safe(inputs)
