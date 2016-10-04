from django.conf.urls import url, include
from django.contrib import admin
from booking import views

booking = [
	url(r'^$', views.BookingDetailView.as_view(), name='detail'),
    url(r'^setstate/$', views.BookingSetStateView.as_view(), name='setstate'),
    url(r'^offerrequest/$', views.BookingOfferRequestView.as_view(), name='offerrequest'),
    url(r'^change/$', views.BookingUpdateView.as_view(), name='change'),
	url(r'^report/edit/$', views.BookingReportCreateView.as_view(), name='report_edit'),
]

urlpatterns = [
	url(r'^$', views.BookingListView.as_view(), name='list'),
	url(r'^create/$', views.BookingCreateView.as_view(), name='create'),
	url(r'^(?P<booking>\d+)/', include(booking)),
]
