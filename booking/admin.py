from django.contrib import admin
from booking import models

@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('band', 'venue', 'user', 'begin', 'end', 'state',)

@admin.register(models.BookingEvent)
class BookingEventAdmin(admin.ModelAdmin):
	pass
