from .models import Reservation
from django import forms
from django.forms import DateInput
import datetime

INTERVALS = [
    (datetime.time(hour=x, minute=y), '{:02d}:{:02d}'.format(x, y))
    for x in range(11, 21)
    for y in range(0, 60, 15)
]


class DateInputType(DateInput):
    input_type = 'date'


class ReserveTableForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('__all__')
        widgets = {
            'Date': DateInputType(),
            'time': forms.Select(choices=INTERVALS)
        }
