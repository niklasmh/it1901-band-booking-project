from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from json_views.views import JsonListMixin, JsonDetailMixin, OrderableMixin, FilterMixin
from venue import models

class VenueListView(PermissionRequiredMixin, JsonListMixin, OrderableMixin, ListView):
	permission_required = 'venue.view_venue'
	ordering = 'name'
	model = models.Venue

class VenueDetailView(PermissionRequiredMixin, JsonDetailMixin, FilterMixin, DetailView):
	permission_required = 'venue.view_venue'
	model = models.Venue
	pk_url_kwarg = 'venue_pk'
	slug_url_kwarg = 'venue_slug'
