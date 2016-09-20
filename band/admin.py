from django.contrib import admin
from band import models

@admin.register(models.Band)
class BandAdmin(admin.ModelAdmin):
	list_display = ('name', 'contact_person', 'spotify_artist_id', 'active')
	readonly_fields = ('slug',)
