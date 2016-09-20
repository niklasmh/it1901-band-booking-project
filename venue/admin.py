from django.contrib import admin
from venue import models;

@admin.register(models.Venue)
class VenueAdmin(admin.ModelAdmin):
	list_display = ('name', 'crowd_capacity', 'stage_width', 'stage_depth', 'stage_height', 'active')
	readonly_fields = ('slug',)

