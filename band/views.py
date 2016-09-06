from django.shortcuts import render
from django.views.generic import ListView, DetailView
from band import models
import requests, json

class BandListView(ListView):
	model = models.Band

class BandDetailView(DetailView):
	model = models.Band
	pk_url_kwarg = 'band'
