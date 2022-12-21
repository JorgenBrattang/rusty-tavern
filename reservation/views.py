from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.views import generic, View
from .models import Reservation
from .forms import ReserveTableForm


class ReservationList(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.order_by('-Date')
    template_name = 'view_reservation.html'


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
