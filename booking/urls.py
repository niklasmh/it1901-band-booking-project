from django.conf.urls import url, include
from django.contrib import admin
from booking import views

booking = [
	url(r'^$', views.BookingDetailView.as_view(), name='detail'),
    url(r'^transition/$', views.BookingTransitionView.as_view(), name='transition'),
    url(r'^change/$', views.BookingUpdateView.as_view(), name='change'),
	url(r'^report/edit/$', views.BookingReportCreateView.as_view(), name='report_edit'),
	url(r'^tecnicalreq/add/$', views.TechnicalRequirementCreateView.as_view(), name='techreq_add'),
]

urlpatterns = [
	url(r'^$', views.BookingListView.as_view(), name='list'),
	url(r'^create/$', views.BookingCreateView.as_view(), name='create'),
	url(r'^(?P<booking>\d+)/', include(booking)),
]
