from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('menu.urls'), name='menu.urls'),
    path('accounts/', include('allauth.urls')),
    path('reserve_table/', include('reservation.urls'), name='reservation.urls'),
]
