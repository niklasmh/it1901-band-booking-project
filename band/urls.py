from django.conf.urls import url, include
from django.contrib import admin
from band import views

band = [
	url(r'^$', views.BandDetailView.as_view(), name='detail'),
	url(r'^update/$', views.BandUpdateView.as_view(), name='update'),
]

urlpatterns = [
	url(r'^$', views.BandListView.as_view(), name='list'),
	url(r'^create/$', views.BandCreateView.as_view(), name='create'),
	url(r'^(?P<band>\d+)/', include(band)),
]
