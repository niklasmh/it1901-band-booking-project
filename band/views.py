from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from json_views.views import JsonListMixin, JsonDetailMixin, OrderableMixin, FilterMixin
from band import models
import requests, json

class BandListView(JsonListMixin, OrderableMixin, FilterMixin, ListView):
	ordering = 'name'
	allowed_filters = {
		"genre": "genres__name"
	}
	model = models.Band

class BandDetailView(JsonDetailMixin, DetailView):
	model = models.Band
	pk_url_kwarg = 'band_pk'
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
				popularitet = context['band_meta']['popularity']
				valueString = ''
				if popularitet >= 90:
						valueString = 'Extremely popular'
				elif popularitet >= 80:
						valueString = 'High popular'
				elif popularitet >= 70:
						valueString = 'Above medium popular'
				elif popularitet >=40:
						valueString = 'Medium popular'
				elif popularitet >= 20:
						valueString = 'Under medium popular.'
				else:
						valueString = 'Not popular band'

				context['band_meta']['popularity_verdi'] = valueString

			artist_req = requests.get('https://api.spotify.com/v1/artists/%s/top-tracks?country=NO' % (
				self.object.spotify_artist_id
			))

			if artist_req.status_code == 200:
				data = json.loads(artist_req.content.decode('utf8'))
				context['song_ids'] = ','.join(track['id'] for track in data['tracks'])

		return context

class BandCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'band.add_band'
	model = models.Band
	fields = ('name', 'contact_person', 'contact_phone', 'contact_email', 'spotify_artist_id', 'active')

	def form_valid(self, form):
		search_req = requests.get('https://api.spotify.com/v1/search?q=%s&type=artist&market=NO&limit=1' % (
			escape_uri_path(form.cleaned_data['name'])
		))
		if search_req.status_code == 200:
			data = json.loads(search_req.content.decode('utf8'))
			if data['artists']['items']:
				artist = data['artists']['items'][0]
				form.instance.spotify_artist_id = artist['id']
				form.instance.save()
				for genre in range(0,len(artist['genres'])):
					if models.Genre.objects.filter(name=artist['genres'][genre]).exists():
						models.Genre.objects.get(name=artist['genres'][genre]).bands.add(form.instance)
					else:
						g = models.Genre(name=artist['genres'][genre])
						g.save()
						models.Genre.objects.get(name=artist['genres'][genre]).bands.add(form.instance)
			return super(BandCreateView, self).form_valid(form)

class BandUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'band.edit_band'
	model = models.Band
	pk_url_kwarg = 'band_pk'
	slug_url_kwarg = 'band_slug'
	fields = '__all__'
