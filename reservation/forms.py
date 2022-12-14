from .models import Reservation
from django import forms
from django.forms import DateInput
from django_flatpickr.widgets import DatePickerInput
import datetime

INTERVALS = [
    (datetime.time(hour=x, minute=y), '{:02d}:{:02d}'.format(x, y))
    for x in range(11, 21)
    for y in range(0, 60, 15)
]


class ReserveTableForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('name', 'phone', 'table_for', 'Date', 'time')
        widgets = {
            'Date': DatePickerInput(),
            'time': forms.Select(choices=INTERVALS)
        }
