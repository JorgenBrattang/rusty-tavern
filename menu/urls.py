from . import views
from django.urls import path

urlpatterns = [
    path('', views.ItemList.as_view(), name='home')
]
