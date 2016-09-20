from django import forms
class BookingSetStateForm(forms.Form): 
    accepted = forms.BooleanField(required = False) 
    rejected = forms.BooleanField(required = False) 