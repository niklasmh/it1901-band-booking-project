from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from band import models
import requests, json

class BandListView(ListView):
	model = models.Band

class BandDetailView(DetailView):
	model = models.Band
	pk_url_kwarg = 'band'

	def get_context_data(self, **kwargs):
		context = super(BandDetailView, self).get_context_data(**kwargs)
		if self.object.spotify_artist_id:
			artist_req = requests.get('https://api.spotify.com/v1/artists/%s/' % (
				self.object.spotify_artist_id
			))
			if artist_req.status_code == 200:
				context['band_meta'] \
					= json.loads(artist_req.content.decode('utf8'))
		return context

class BandCreateView(CreateView):
	model = models.Band
	fields = '__all__'

class BandUpdateView(UpdateView):
	model = models.Band
	pk_url_kwarg = 'band'
	fields = '__all__'
