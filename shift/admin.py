from django.contrib import admin
from shift import models

@admin.register(models.Group)
class ShiftGroupAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Shift)
class ShiftAdmin(admin.ModelAdmin):
	list_display = ('name', 'booking', 'group', 'user',)

@admin.register(models.DefaultShiftSet)
class DefaultShiftSetAdmin(admin.ModelAdmin):
	list_display = ('name', 'venue',)

@admin.register(models.DefaultShift)
class DefaultShiftAdmin(admin.ModelAdmin):
	list_display = ('name', 'shiftset', 'group',)
