from django.contrib import admin
from shift import models

@admin.register(models.Group)
class ShiftGroupAdmin(admin.ModelAdmin):
	pass

@admin.register(models.Shift)
class ShiftAdmin(admin.ModelAdmin):
	pass

@admin.register(models.DefaultShiftSet)
class DefaultShiftSetAdmin(admin.ModelAdmin):
	pass

@admin.register(models.DefaultShift)
class DefaultShiftAdmin(admin.ModelAdmin):
	pass
