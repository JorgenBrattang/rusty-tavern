from . import views
from django.urls import path

urlpatterns = [
    path('', views.ItemList.as_view(), name='home'),
    path('<slug:slug>/', views.ItemDetail.as_view(), name='item_detail'),
]
