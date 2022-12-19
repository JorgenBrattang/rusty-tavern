from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from .models import Reservation
from .forms import ReserveTableForm


def Reserv_table(request):
    form = ReserveTableForm()

    if request.method == 'POST':
        form = ReserveTableForm(request.POST)
        if form.is_valid():
            form.save()

            context = {
                'form': form,
                'reserved': True,
            }

    if request.method == 'GET':
        context = {
            'form': form,
            'reserved': False,
        }

    return render(request, 'reservations.html', context)
