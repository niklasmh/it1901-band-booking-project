from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render
from venue import models

class VenueListView(ListView):
	model = models.Venue

class VenueDetailView(DetailView):
	model = models.Venue
	pk_url_kwarg = 'venue_pk'
	slug_url_kwarg = 'venue_slug'
