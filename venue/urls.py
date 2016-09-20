from django.conf.urls import url, include
from venue import views

venue = [
	url(r'^$', views.VenueDetailView.as_view(), name='detail'),
]

urlpatterns = [
	url(r'^$', views.VenueListView.as_view(), name='list'),
	url(r'^(?P<venue_pk>\d+)/', include(venue)),
	url(r'^(?P<venue_slug>[-a-zA-Z0-9]+)/', include(venue)),
]
