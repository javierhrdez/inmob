from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ageb', views.ageb, name='ageb'),
    path('propiedades', views.propiedades, name='propiedades'),
    path('buffer', views.buffer, name='buffer'),
    path('ageb_buffer', views.ageb_buffer, name='ageb_buffer'),
    path('propiedades_buffer', views.propiedades_buffer, name='propiedades_buffer'),
    path('geocoding', views.geocoding, name='geocoding'),
]
