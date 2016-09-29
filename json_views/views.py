from django.forms.models import model_to_dict
from django.http import JsonResponse

class JsonBaseMixin:
	json_response_class = JsonResponse
	response_type = 'text/http'
	accepted_types = ['text/http', 'text/json']
	def dispatch(self, response, *args, **kwargs):
		accept = response.META.get('HTTP_ACCEPT', 'text/html').split(',')
		for t in accept:
			if t in self.accepted_types:
				self.response_type = t
				break
		return super(JsonBaseMixin, self).dispatch(response, *args, **kwargs)

	def render_to_response(self, context, **response_kwargs):
		if not self.response_class or self.response_type != 'text/json':
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