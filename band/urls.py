from django.conf.urls import url, include
from django.contrib import admin
from band import views

band = [
	url(r'^$', views.BandDetailView.as_view(), name='detail'),
]

urlpatterns = [
	url(r'^$', views.BandListView.as_view(), name='list'),
	url(r'^(?P<band>\d+)/', include(band)),
]
