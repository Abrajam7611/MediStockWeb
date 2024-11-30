# apps/ventas_realizadas/views.py
from django.shortcuts import render
from firebase_admin import firestore
from datetime import datetime

db = firestore.client()

def ventas_realizadas_view(request):
    # Obtener las ventas realizadas desde Firestore
    ventas_realizadas_ref = db.collection('ventas').stream()
    ventas_realizadas = []
    for venta in ventas_realizadas_ref:
        venta_data = venta.to_dict()
        ventas_realizadas.append({
            'nombre': venta_data['nombre'],
            'cantidad': venta_data['cantidad'],
            'precio': venta_data['precio'],
            'total': venta_data['total'],
            'fecha': venta_data['fecha']
        })

    # Organizar las ventas por fecha
    ventas_realizadas.sort(key=lambda x: x['fecha'], reverse=True)

    return render(request, 'ventas_realizadas/ventas_realizadas.html', {
        'ventas_realizadas': ventas_realizadas
    })
