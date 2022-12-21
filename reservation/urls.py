from . import views
from django.urls import path

urlpatterns = [
    path('', views.Reserv_table, name='reserve_table'),
    path('view_reservation/', views.ReservationList.as_view(),
         name='view_reservation')
]
