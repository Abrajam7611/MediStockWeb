from django.shortcuts import render, redirect
from .forms import ProductoForm
from firebase_services import get_productos, agregar_producto, obtener_producto, editar_producto, eliminar_producto

def crear_producto_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Agrega el producto a Firebase
            agregar_producto(form.cleaned_data)
            return redirect('inventario')
    else:
        form = ProductoForm()
    return render(request, 'inventario/crear_producto.html', {'form': form})

def editar_producto_view(request, producto_id):
    # Obtén el producto desde Firebase
    producto = obtener_producto(producto_id)
    if not producto:
        return redirect('inventario')  # Si no se encuentra el producto, redirige al inventario
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, initial=producto)
        if form.is_valid():
            # Limpia los datos del formulario para Firebase
            cleaned_data = form.cleaned_data
            try:
                # Edita el producto en Firebase
                editar_producto(producto_id, cleaned_data)
                return redirect('inventario')  # Redirige a la vista de inventario después de editar
            except Exception as e:
                return render(request, 'inventario/editar_producto.html', {
                    'form': form,
                    'producto_id': producto_id,
                    'error_message': f'Error al editar el producto: {e}'
                })
    else:
        form = ProductoForm(initial=producto)

    return render(request, 'inventario/editar_producto.html', {'form': form, 'producto_id': producto_id})

def eliminar_producto_view(request, producto_id):
    try:
        eliminar_producto(producto_id)
    except Exception as e:
        return render(request, 'inventario/inventario.html', {
            'error_message': f'Error al eliminar producto: {e}'
        })
    return redirect('inventario')

def inventario_view(request):
    productos = get_productos()  # Obtén todos los productos desde Firebase
    return render(request, 'inventario/inventario.html', {'productos': productos})
