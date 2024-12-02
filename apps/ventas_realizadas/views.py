from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import firebase_admin
from firebase_admin import firestore
from django.core.paginator import Paginator


# Inicializar la aplicación Firebase (si no se ha inicializado aún)
if not firebase_admin._apps:
    firebase_admin.initialize_app()

# Conexión a Firestore
db = firestore.client()

def ventas_realizadas_view(request):
    """
    Vista para mostrar las ventas realizadas desde Firestore en una plantilla con paginación.
    """
    # Obtener las ventas realizadas desde Firestore
    ventas_realizadas_ref = db.collection('ventas').stream()
    ventas_realizadas = []
    
    # Filtrar las ventas según la fecha seleccionada
    filtro_fecha = request.GET.get('filtro_fecha', None)
    
    for venta in ventas_realizadas_ref:
        venta_data = venta.to_dict()

        # Obtener la fecha, si es un Timestamp se convierte automáticamente a datetime
        fecha_venta = venta_data['fecha']
        
        if isinstance(fecha_venta, datetime):
            pass  # Ya es un datetime
        else:
            # Si es un Timestamp de Firestore, se convierte a datetime
            fecha_venta = fecha_venta.to_datetime()  # Firestore Timestamp a datetime

        # Agregar la venta al listado
        ventas_realizadas.append({
            'nombre': venta_data['nombre'],
            'cantidad': venta_data['cantidad'],
            'precio': venta_data['precio'],
            'total': venta_data['total'],
            'fecha': fecha_venta
        })

    # Si hay un filtro de fecha, filtrar las ventas
    if filtro_fecha:
        fecha_filtrada = datetime.strptime(filtro_fecha, "%Y-%m-%d")
        ventas_realizadas = [venta for venta in ventas_realizadas if venta['fecha'].date() == fecha_filtrada.date()]

    # Ordenar las ventas por fecha en orden descendente
    ventas_realizadas.sort(key=lambda x: x['fecha'], reverse=True)

    # Paginación
    paginator = Paginator(ventas_realizadas, 7)  # Mostrar 8 ventas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con los datos de las ventas y la paginación
    return render(request, 'ventas_realizadas/ventas_realizadas.html', {
        'page_obj': page_obj
    })

def generar_reporte_pdf(request):
    """
    Vista para generar un archivo PDF con el reporte de ventas realizadas.
    """
    # Obtener las ventas realizadas desde Firestore
    ventas_realizadas_ref = db.collection('ventas').stream()
    ventas_realizadas = []
    
    # Obtener la fecha del filtro desde la URL
    filtro_fecha = request.GET.get('filtro_fecha', None)

    # Si no se proporciona un filtro de fecha, se filtran todas las ventas
    if filtro_fecha:
        # Convertir la fecha seleccionada en un objeto datetime
        fecha_filtrada = datetime.strptime(filtro_fecha, "%Y-%m-%d")
    
    # Recorrer todas las ventas y filtrar por la fecha seleccionada
    for venta in ventas_realizadas_ref:
        venta_data = venta.to_dict()
        
        # Obtener la fecha, si es un Timestamp se convierte automáticamente a datetime
        fecha_venta = venta_data['fecha']
        
        # Asegúrate de que fecha_venta sea de tipo datetime
        if isinstance(fecha_venta, datetime):
            # No se necesita hacer nada, ya es un datetime
            pass
        else:
            # Si es un Timestamp de Firestore, se convierte a datetime
            fecha_venta = fecha_venta.to_datetime()  # Firestore Timestamp a datetime
        
        # Si hay un filtro de fecha, filtrar las ventas por la fecha seleccionada
        if filtro_fecha and fecha_venta.date() == fecha_filtrada.date():
            ventas_realizadas.append({
                'nombre': venta_data['nombre'],
                'cantidad': venta_data['cantidad'],
                'precio': venta_data['precio'],
                'total': venta_data['total'],
                'fecha': fecha_venta
            })
        elif not filtro_fecha:
            ventas_realizadas.append({
                'nombre': venta_data['nombre'],
                'cantidad': venta_data['cantidad'],
                'precio': venta_data['precio'],
                'total': venta_data['total'],
                'fecha': fecha_venta
            })

    # Crear la respuesta HTTP para el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_ventas_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pdf"'

    # Crear el documento PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Título
    p.drawString(200, 750, "Reporte de Ventas Realizadas")
    p.drawString(200, 730, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Encabezados de las columnas
    p.drawString(30, 700, "Nombre")
    p.drawString(180, 700, "Cantidad")
    p.drawString(250, 700, "Precio")
    p.drawString(320, 700, "Total")
    p.drawString(400, 700, "Fecha")

    # Línea para separar los encabezados de los datos
    p.line(20, 690, 580, 690)

    # Agregar los datos de las ventas filtradas
    y_position = 670  # Posición inicial vertical
    for venta in ventas_realizadas:
        if y_position < 40:  # Si se llega al final de la página, se añade una nueva página
            p.showPage()
            p.setFont("Helvetica", 12)
            y_position = 750

        p.drawString(30, y_position, str(venta['nombre']))
        p.drawString(180, y_position, str(venta['cantidad']))
        p.drawString(250, y_position, f"${venta['precio']}")
        p.drawString(320, y_position, f"${venta['total']}")
        p.drawString(400, y_position, venta['fecha'].strftime("%d/%m/%Y %H:%M"))

        y_position -= 20  # Desplazar hacia abajo para la siguiente fila

    p.save()

    return response
