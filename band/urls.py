from django.conf.urls import url, include
from django.contrib import admin
from band import views

band = [
	url(r'^$', views.BandDetailView.as_view(), name='detail'),
	url(r'^update/$', views.BandUpdateView.as_view(), name='update'),
	url(r'^member/add/$', views.BandCreateMemberView.as_view(), name='member_add'),
]

urlpatterns = [
	url(r'^$', views.BandListView.as_view(), name='list'),
	url(r'^create/$', views.BandCreateView.as_view(), name='create'),
	url(r'^(?P<band_pk>\d+)/', include(band)),
	url(r'^(?P<band_slug>[-a-zA-Z0-9]+)/', include(band)),
]
