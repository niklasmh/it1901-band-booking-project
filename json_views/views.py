from django.forms.models import model_to_dict
from django.http import JsonResponse
import re

class JsonBaseMixin:
	json_response_class = JsonResponse
	response_type = 'text/http'
	accepted_types = ['text/http', 'application/json']
	def dispatch(self, response, *args, **kwargs):
		accept = response.META.get('HTTP_ACCEPT', 'text/html').split(',')
		for t in accept:
			if t in self.accepted_types:
				self.response_type = t
				break
		return super(JsonBaseMixin, self).dispatch(response, *args, **kwargs)

	def render_to_response(self, context, **response_kwargs):
		if not self.response_class or self.response_type != 'application/json':
			return super(JsonBaseMixin, self).render_to_response(context, **response_kwargs)

		return self.json_response_class({
			'object': self.get_object_dict()
		}, **response_kwargs)

	def get_object_dict(self):
		pass

class JsonListMixin(JsonBaseMixin):
	fields = None
	exclude = None
	def get_object_dict(self):
		return [ self.serialize(obj) for obj in self.get_queryset() ]

	def serialize(self, obj):
		return model_to_dict(obj, fields=self.fields, exclude=self.exclude)

class JsonDetailMixin(JsonBaseMixin):
	fields = None
	exclude = None
	def get_object_dict(self):
		return self.serialize(self.get_object())

	def serialize(self, obj):
		return model_to_dict(obj, fields=self.fields, exclude=self.exclude)

class OrderableMixin(object):
	orderable_fields = '__all__'
	def get_ordering(self):
		order = self.request.GET.get('order', self.ordering)
		if self.orderable_fields == '__all__':
			return order
		m = re.match('-?([0-9a-zA-Z_]+)', order)
		if m and m.group(1) in self.orderable_fields:
			return order
		return self.ordering

class FilterMixin(object):
	allowed_filters = {}
	def get_queryset(self):
		qs = super(FilterMixin, self).get_queryset()
		filters = {}
		for field in self.allowed_filters:
			if field in self.request.GET:
				filters[self.allowed_filters[field]] = self.request.GET.get(field)
		qs = qs.filter(**filters)
		return qs
