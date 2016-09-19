from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS += [compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware(object):
	def __init__(self):
		pass

	def process_request(self, request):
		assert not hasattr(self, 'user'), "The LoginRequiredMiddleware requires the AuthenticationMiddleware to be run first"
		if not request.user.is_authenticated():
			path = request.path_info.lstrip('/')
			if not any(m.match(path) for m in EXEMPT_URLS):
				return redirect_to_login(request.path_info)
