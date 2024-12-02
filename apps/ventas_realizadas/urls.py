# apps/ventas_realizadas/urls.py
from django.urls import path
from . import views
from .views import ventas_realizadas_view, generar_reporte_pdf


urlpatterns = [
    path('', views.ventas_realizadas_view, name='ventas_realizadas'),  # Verifica el nombre 'ventas_realizadas'
    path('reporte-pdf/', views.generar_reporte_pdf, name='reporte_pdf'),  # Nueva ruta para el reporte PDF

]
