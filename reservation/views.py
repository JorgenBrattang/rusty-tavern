from django.shortcuts import render
from .models import Reservation
from .forms import ReserveTableForm

def Reserv_table(request):
    form = ReserveTableForm()

    if request.method == 'POST':
        form = ReserveTableForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    
    return render(request, 'reservations.html', context)
