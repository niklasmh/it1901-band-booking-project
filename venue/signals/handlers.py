from django.db.models.signals import pre_save
from django_unique_slugify import unique_slugify
from venue import models

def add_venue_slug(instance, **kwargs):
	if not instance.slug:
		unique_slugify(instance, instance.name, queryset=models.Venue.objects.all())

pre_save.connect(add_venue_slug, sender=models.Venue)
