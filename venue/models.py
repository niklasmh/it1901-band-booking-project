from django.db import models

class Venue(models.Model):
	name = models.CharField(max_length=200)
	crowd_capacity = models.IntegerField()
	stage_width = models.DecimalField(max_digits=10, decimal_places=2)
	stage_depth = models.DecimalField(max_digits=10, decimal_places=2)
	stage_height = models.DecimalField(max_digits=10, decimal_places=2)
	active = models.BooleanField(default=True)
