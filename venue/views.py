from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render
from json_views.views import JsonListMixin, JsonDetailMixin, OrderableMixin, FilterMixin
from venue import models

class VenueListView(JsonListMixin, OrderableMixin, ListView):
	ordering = 'name'
	model = models.Venue

class VenueDetailView(JsonDetailMixin, FilterMixin, DetailView):
	model = models.Venue
	pk_url_kwarg = 'venue_pk'
	slug_url_kwarg = 'venue_slug'
