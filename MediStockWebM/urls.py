from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from apps.usuarios import views as usuarios_views
from apps.inicio import views as inicio_views
from apps.ventas import views as ventas_views
from apps.inventario import views as inventario_views

urlpatterns = [
    path('', usuarios_views.login_view, name='login'),  # Ruta para login
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('inicio/', inicio_views.inicio_view, name='inicio'),  # Ruta para la página de inicio
    path('ventas/', ventas_views.ventas_view, name='ventas'),  # Ruta para las ventas
    path('ventas-realizadas/', include('apps.ventas_realizadas.urls')),  # Este es el include de ventas_realizadas
    path('inventario/', include('apps.inventario.urls')),  # Incluye las rutas de inventario
    path('logout/', LogoutView.as_view(), name='logout'),  # Ruta para cerrar sesión
]