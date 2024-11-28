# apps/ventas/views.py
from django.shortcuts import render

def ventas_view(request):
    return render(request, 'ventas.html')
