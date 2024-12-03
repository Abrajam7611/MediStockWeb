from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.core.paginator import Paginator
from firebase_services import get_productos, agregar_producto, obtener_producto, editar_producto, eliminar_producto

def crear_producto_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Agrega el producto a Firebase
            try:
                agregar_producto(form.cleaned_data)
                return redirect('inventario')  # Redirige a la vista de inventario
            except Exception as e:
                # Si ocurre un error al agregar, se muestra el mensaje de error
                return render(request, 'inventario/crear_producto.html', {
                    'form': form,
                    'error_message': f'Error al agregar el producto: {e}'
                })
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/crear_producto.html', {'form': form})

def editar_producto_view(request, producto_id):
    producto = obtener_producto(producto_id)  # Obtén el producto desde Firebase
    if not producto:
        return redirect('inventario')  # Si no se encuentra el producto, redirige al inventario
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, initial=producto)
        if form.is_valid():
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
        eliminar_producto(producto_id)  # Elimina el producto de Firebase
    except Exception as e:
        return render(request, 'inventario/inventario.html', {
            'error_message': f'Error al eliminar producto: {e}'
        })
    return redirect('inventario')  # Redirige a la vista de inventario después de eliminar

def inventario_view(request):
    productos = get_productos()  # Obtén todos los productos desde Firebase
    
    # Paginación: 5 productos por página
    paginator = Paginator(productos, 5)
    page_number = request.GET.get('page')  # Obtiene el número de página
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual

    return render(request, 'inventario/inventario.html', {'productos': page_obj})