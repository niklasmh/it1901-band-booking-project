from django.views.generic import FormView, RedirectView
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

class LoginView(FormView):
	template_name = 'user/login.html'
	success_url = reverse_lazy('index')
	form_class = AuthenticationForm
	redirect_field_name = REDIRECT_FIELD_NAME

	@method_decorator(sensitive_post_parameters('password'))
	def dispatch(self, request, *args, **kwargs):

		if request.user.is_authenticated():
			return HttpResponseRedirect(self.get_success_url())

		request.session.set_test_cookie()

		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		auth_login(self.request, form.get_user())

		if self.request.session.test_cookie_worked():
			self.request.session.delete_test_cookie()

		return super(LoginView, self).form_valid(form)

	def get_success_url(self):
		redirect_to = self.request.GET.get(self.redirect_field_name)
		if not is_safe_url(url=redirect_to, host=self.request.get_host()):
			redirect_to = self.success_url
		return redirect_to

class LogoutView(RedirectView):
	url = settings.LOGIN_URL

	def get(self, request, *args, **kwargs):
		auth_logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)

class PasswordChangeView(FormView):
	form_class = PasswordChangeForm
	template_name = 'user/change_password.html'
	success_url = reverse_lazy('index')

	@method_decorator(sensitive_post_parameters('old_password', 'new_password1', 'new_password2'))
	def dispatch(self, request, *args, **kwargs):
		return super(PasswordChangeView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(PasswordChangeView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form.save()
		return super(PasswordChangeView, self).form_valid(form)
