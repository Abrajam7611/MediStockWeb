# apps/ventas_realizadas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ventas_realizadas_view, name='ventas_realizadas'),  # Verifica el nombre 'ventas_realizadas'
]
