# apps/ventas/urls.py
from django.urls import path
from .views import ventas_view

urlpatterns = [
    path('', ventas_view, name='ventas'),  # Ruta principal para ventas
]
