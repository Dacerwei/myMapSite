from django import forms
from datetime import datetime


class dateSearch(forms.Form):
	from_date = forms.DateField()
	to_date = forms.DateField()
