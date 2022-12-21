from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'table_for',
        'Date',
        'time'
    )
