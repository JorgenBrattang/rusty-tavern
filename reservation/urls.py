from . import views
from django.urls import path

urlpatterns = [
    path('', views.Reserv_table, name='reserve_table'),
]
