from django.contrib.auth.views import login, logout, password_change
from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^band/', include('band.urls', namespace='band')),
    url(r'^venue/', include('venue.urls', namespace='venue')),
    url(r'^booking/', include('booking.urls', namespace='booking')),
    url(r'^shift/', include('shift.urls', namespace='shift')),
    url(r'^admin/', admin.site.urls),
]
