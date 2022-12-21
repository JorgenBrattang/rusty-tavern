from . import views
from django.urls import path

urlpatterns = [
    path('', views.add_reservation,
         name='add_reservation'),
    path('view/', views.ReservationList.as_view(),
         name='view_reservation'),
    path('edit/<pk>', views.edit_reservation,
         name='edit_reservation'),
    path('delete/<pk>', views.delete_reservation,
         name='delete_reservation'),
]
