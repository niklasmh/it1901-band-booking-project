from django.db.models.signals import pre_save, post_save
from booking import models

def booking_created_log(instance, created, **kwargs):
	if created:
		event = models.BookingEvent(booking=instance,
									event_type=models.BOOKING_EVENT_CREATE,
									user=instance.user)
		event.save()

post_save.connect(booking_created_log, sender=models.Booking)
