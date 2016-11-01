from django.shortcuts import render, get_object_or_404
from django.utils.encoding import escape_uri_path
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from json_views.views import JsonListMixin, JsonDetailMixin, OrderableMixin, FilterMixin
from django.contrib.auth.models import User
from django.urls import reverse
from band import models, forms
import requests, json

class BandMemberViewableMixin:
	def has_permission(self):
		perm = super(BandMemberViewableMixin, self).has_permission()
		manager_perm = self.request.user.has_perms(['band.view_managing_bands'])
		self.is_manager = manager_perm and self.is_manager_for_object() and not perm
		return perm or self.is_manager
	def is_manager_for_object(self):
		return True
	def get_context_data(self, **kwargs):
		context = super(BandMemberViewableMixin, self).get_context_data(**kwargs)
		context['is_manager'] = self.is_manager
		return context

class BandListView(BandMemberViewableMixin, PermissionRequiredMixin, JsonListMixin, OrderableMixin, FilterMixin, ListView):
	permission_required = 'band.view_band'
	ordering = 'name'
	fields = ('id', 'name', 'contact_person', 'contact_phone', 'contact_email', 'spotify_artist_id', 'slug', 'concerts', 'sold_albums')
	allowed_filters = {
		"genre": "genres__name"
	}
	model = models.Band

	def get_queryset(self):
		qs = super(BandListView, self).get_queryset()
		if self.is_manager:
			qs = qs.filter(members__id=self.request.user.id)
		return qs

class BandDetailView(BandMemberViewableMixin, PermissionRequiredMixin, JsonDetailMixin, DetailView):
	permission_required = 'band.view_band'
	model = models.Band
	pk_url_kwarg = 'band_pk'
	slug_url_kwarg = 'band_slug'
	fields = ('id', 'name', 'contact_person', 'contact_phone', 'contact_email', 'spotify_artist_id', 'slug', 'concerts', 'sold_albums')

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

	def is_manager_for_object(self):
		obj = get_object_or_404(models.Band, **({'id':self.kwargs['band_pk']} if 'band_pk' in self.kwargs else {'slug':self.kwargs['band_slug']}))
		return self.request.user in obj.members.all()

class BandCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'band.add_band'
	model = models.Band
	fields = ('name', 'contact_person', 'contact_phone', 'contact_email', 'spotify_artist_id', 'concerts','sold_albums','active',)

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

class BandCreateMemberView(PermissionRequiredMixin, CreateView):
	template_name = 'band/user_form.html'
	permission_required = 'band.add_band'
	model = User
	#fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
	form_class = forms.ManagerUserCreationForm
	def get_context_data(self, **kwargs):
		context = super(BandCreateMemberView, self).get_context_data(**kwargs)
		context['band'] = self.band
		return context
		
	def dispatch(self, request, *args, **kwargs):
		dt = {'slug': kwargs.get('band_slug')} if 'band_slug' in kwargs else {'id': kwargs.get('band_pk')}
		self.band = models.Band.objects.get(**dt)
		return super(BandCreateMemberView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		form.instance.is_active = True
		ret = super(BandCreateMemberView, self).form_valid(form)
		self.band.members.add(self.object)
		return ret

	def get_success_url(self):
		return reverse('band:detail', kwargs=self.kwargs)

