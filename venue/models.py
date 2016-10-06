from django.db import models

class Venue(models.Model):
	name = models.CharField(max_length=200)
	crowd_capacity = models.IntegerField()
	stage_width = models.DecimalField(max_digits=10, decimal_places=2)
	stage_depth = models.DecimalField(max_digits=10, decimal_places=2)
	stage_height = models.DecimalField(max_digits=10, decimal_places=2)
	active = models.BooleanField(default=True)
	slug = models.SlugField(null=True, editable=False)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('venue:detail', kwargs={ 'venue_slug': self.slug })

	def get_bookings(self):
		return self.bookings.exclude(report__isnull=True)
