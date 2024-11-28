from django import forms
from datetime import datetime

class ProductoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea)
    fecha_caducidad = forms.DateTimeField(widget=forms.SelectDateWidget(years=range(2024, 2030)))
    lote = forms.CharField(max_length=50)
    precio = forms.DecimalField(max_digits=10, decimal_places=2)
    presentacion = forms.CharField(max_length=100)
    stock = forms.IntegerField()
    sustancia = forms.CharField(max_length=100)

    def clean_fecha_caducidad(self):
        # Convierte la fecha a un objeto datetime si es necesario
        fecha = self.cleaned_data['fecha_caducidad']
        if isinstance(fecha, datetime):
            return fecha.replace(tzinfo=None)  # Elimina la zona horaria si es necesario
        return fecha
