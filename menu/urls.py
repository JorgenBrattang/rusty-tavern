from . import views
from django.urls import path

urlpatterns = [
    path('', views.ItemList_short.as_view(), name='home'),
    path('menu/', views.ItemList.as_view(), name='menu'),
    path('menu/<slug:slug>/', views.ItemDetail.as_view(), name='item_detail'),
    path('menu/like/<slug:slug>', views.ItemLike.as_view(), name='item_like'),
]
