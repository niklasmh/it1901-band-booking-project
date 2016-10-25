from django.conf.urls import url, include
from shift import views

urlpatterns = [
	url(r'^$', views.ShiftListView.as_view(), name='list'),
]
