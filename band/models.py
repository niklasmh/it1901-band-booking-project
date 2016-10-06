from django.db import models
from django.urls import reverse

class Band(models.Model):
	name = models.CharField(max_length=200)
	contact_person = models.CharField(max_length=200, blank=True, null=True)
	contact_phone = models.PositiveIntegerField(blank=True, null=True)
	contact_email = models.EmailField(max_length=30, blank=True, null=True)
	spotify_artist_id = models.CharField(max_length=50, blank=True, null=True)
	active = models.BooleanField(default=True)
	slug = models.SlugField(null=True, editable=False)
	concerts = models.PositiveIntegerField(default=0)
	sold_albums = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('band:detail', kwargs={ 'band_slug': self.slug })

	def get_genres(self):
		return ', '.join([str(i.name) for i in self.genres.all()][:3])

	def get_all_genres(self):
		return ', '.join([str(i.name) for i in self.genres.all()])

class Genre(models.Model):
	name = models.CharField(max_length=50)
	bands = models.ManyToManyField(Band, related_name="genres")

	def __str__(self):
		return self.name
