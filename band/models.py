from django.db import models
from django.urls import reverse

class Band(models.Model):
	name = models.CharField(max_length=200)
	contact_person = models.CharField(max_length=200, blank=True, null=True)
	contact_phone = models.CharField(max_length=30, blank=True, null=True)
	contact_email = models.CharField(max_length=30, blank=True, null=True)
	spotify_artist_id = models.CharField(max_length=50, blank=True, null=True)
	genres = models.CharField(max_length=200, blank=True, null=True)
	active = models.BooleanField(default=True)
	slug = models.SlugField(null=True, editable=False)
	concerts = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('band:detail', kwargs={ 'band_slug': self.slug })
