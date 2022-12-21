from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'number_of_persons',
        'Date',
        'time'
    )
