from django.contrib.auth.views import login, logout, password_change
from django.conf.urls import url
from user import views

urlpatterns = [
	url(r'^login/$', views.LoginView.as_view(), name='login'),
	url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
	url(r'^password/$', views.PasswordChangeView.as_view(), name='changepassword'),
]
