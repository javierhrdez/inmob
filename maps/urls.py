from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ageb', views.ageb, name='ageb'),
    path('propiedades', views.propiedades, name='propiedades'),
    path('buffer', views.buffer, name='buffer'),
]
