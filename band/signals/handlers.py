from django.db.models.signals import pre_save
from django_unique_slugify import unique_slugify
from band import models

def add_band_slug(instance, **kwargs):
	if not instance.slug:
		unique_slugify(instance, instance.name, queryset=models.Band.objects.all())

pre_save.connect(add_band_slug, sender=models.Band)
