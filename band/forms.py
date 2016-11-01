from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from booking import models

class ManagerUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("username", "first_name", "last_name")
		field_classes = {'username': UsernameField}
