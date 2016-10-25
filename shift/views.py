from django.views.generic import ListView, DetailView, CreateView, UpdateView
from shift import models

class ShiftListView(ListView):
	model = models.Shift

	def get_queryset(self):
		qs = super(ShiftListView, self).get_queryset()
		qs = qs.filter(group__in=self.request.user.shift_groups.all())
		return qs
