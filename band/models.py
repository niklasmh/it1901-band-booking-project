from django.db import models

class Band(models.Model):
	name = models.CharField(max_length=200)
	contact_person = models.CharField(max_length=200, blank=True, null=True)
	contact_phone = models.CharField(max_length=30, blank=True, null=True)
	contact_email = models.CharField(max_length=30, blank=True, null=True)
	spotify_artist_id = models.CharField(max_length=50, blank=True, null=True)
	active = models.BooleanField(default=True)
