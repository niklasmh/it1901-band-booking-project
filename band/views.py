from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from band import models
import requests, json

class BandListView(ListView):
	model = models.Band

class BandDetailView(DetailView):
	model = models.Band
	pk_url_kwarg = 'band'
	slug_url_kwarg = 'band_slug'

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

	def form_valid(self, form):
		search_req = requests.get('https://api.spotify.com/v1/search?q=%s&type=artist&market=NO&limit=1' % (
			escape_uri_path(form.cleaned_data['name'])
		))
		if search_req.status_code == 200:
			data = json.loads(search_req.content.decode('utf8'))
			if data['artists']['items']:
				artist = data['artists']['items'][0]
				form.instance.spotify_artist_id = artist['id']
			return super(BandCreateView, self).form_valid(form)

class BandUpdateView(UpdateView):
	model = models.Band
	pk_url_kwarg = 'band_pk'
	slug_url_kwarg = 'band_slug'
	fields = '__all__'
