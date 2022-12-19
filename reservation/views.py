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

            subject = 'Thank you for your reservation from Rusty Tavern'
            message = 'Your information is here... later'
            from_email = settings.EMAIL_HOST_USER
            to_list = [settings.EMAIL_HOST_USER]

            send_mail(
                subject,
                message,
                from_email,
                to_list,
                False
            )

    if request.method == 'GET':
        context = {
            'form': form,
            'reserved': False,
        }

    return render(request, 'reservations.html', context)
