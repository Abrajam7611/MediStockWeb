# apps/inventario/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('inventario/', views.inventario_view, name='inventario'),
    path('eliminar/<str:producto_id>/', views.eliminar_producto_view, name='eliminar_producto'),
    path('editar/<str:producto_id>/', views.editar_producto_view, name='editar_producto'),
    path('crear/', views.crear_producto_view, name='crear_producto'),

]