from django.shortcuts import render, redirect
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin

# Inicializar Firebase (asegúrate de tener tus credenciales de Firebase)
if not firebase_admin._apps:
    cred = credentials.Certificate('Clave.json')
    firebase_admin.initialize_app(cred)

# Acceso a Firestore
db = firestore.client()

def ventas_view(request):
    # Obtener productos desde Firestore
    productos_ref = db.collection('inventario_producto')
    productos = productos_ref.stream()

    productos_lista = []
    for producto in productos:
        producto_data = producto.to_dict()
        productos_lista.append({
            'id': producto.id,
            'nombre': producto_data['nombre'],
            'precio': producto_data['precio'],
            'stock': producto_data['stock']
        })

    # Cargar carrito desde la sesión
    ventas = request.session.get('ventas', [])
    total = sum(venta['total'] for venta in ventas)  # Calcular total acumulado

    if request.method == 'POST':
        if 'agregar_producto' in request.POST:
            producto_id = request.POST.get('producto_id')
            cantidad = int(request.POST.get('cantidad'))

            # Buscar producto en Firestore
            producto_ref = db.collection('inventario_producto').document(producto_id)
            producto_data = producto_ref.get().to_dict()

            if producto_data:
                # Verificar si el producto ya está en el carrito
                for venta in ventas:
                    if venta['nombre'] == producto_data['nombre']:
                        # Si ya existe, actualizamos la cantidad y total
                        if venta['cantidad'] + cantidad <= producto_data['stock']:
                            venta['cantidad'] += cantidad
                            venta['total'] = venta['cantidad'] * venta['precio']
                        break
                else:
                    # Si no existe, lo agregamos como nuevo
                    if cantidad <= producto_data['stock']:
                        ventas.append({
                            'nombre': producto_data['nombre'],
                            'precio': producto_data['precio'],
                            'cantidad': cantidad,
                            'total': producto_data['precio'] * cantidad,
                        })

                # Actualizar el carrito en la sesión
                request.session['ventas'] = ventas

        elif 'terminar_venta' in request.POST:
            # Registrar la venta en Firebase
            for venta in ventas:
                db.collection('ventas').add({
                    'nombre': venta['nombre'],
                    'cantidad': venta['cantidad'],
                    'precio': venta['precio'],
                    'total': venta['total'],
                    'fecha': firestore.SERVER_TIMESTAMP
                })

            # Limpiar el carrito después de finalizar la venta
            request.session['ventas'] = []
            return redirect('ventas')  # Redirigir después de registrar la venta

        elif 'quitar_producto' in request.POST:
            # Eliminar producto del carrito
            index = int(request.POST.get('quitar_producto'))
            if 0 <= index < len(ventas):
                del ventas[index]
                request.session['ventas'] = ventas  # Actualizar la sesión

    # Recalcular el total después de las operaciones
    total = sum(venta['total'] for venta in ventas)

    # Eliminar la obtención de ventas realizadas desde Firebase
    # Ya no necesitamos esta parte porque no vamos a mostrar las ventas realizadas

    # Regresar solo los productos y el carrito de ventas actuales
    return render(request, 'ventas/ventas.html', {
        'productos': productos_lista,
        'ventas': ventas,
        'total': total,
    })
