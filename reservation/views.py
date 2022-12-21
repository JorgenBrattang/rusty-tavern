from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import Reservation
from .forms import ReserveTableForm


class ReservationList(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.order_by('Date')
    template_name = 'view_reservation.html'


def add_reservation(request):
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

    return render(request, 'add_reservation.html', context)


def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    form = ReserveTableForm(instance=reservation)
    if request.method == 'POST':
        form = ReserveTableForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_reservation'))

    if request.method == 'GET':
        context = {
                    'form': form
                }
    return render(request, 'edit_reservation.html', context)


def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    reservation.delete()
    return HttpResponseRedirect(reverse('view_reservation'))